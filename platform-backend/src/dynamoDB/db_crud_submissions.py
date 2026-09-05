from boto3.dynamodb.conditions import Attr


class DB_CRUD_SUBMISSIONS:
  def __init__(self, submissionTable):
    """Initialize DB_CRUD_SUBMISSIONS class

    Args:
        submissionTable (_type_): db reference to the submission table
    """
    self.__submissionTable = submissionTable

  def __exists(self, idOfTheSubmission: str):
    """Check if the submission exists in the database

    Args:
        idOfTheSubmission (str): id of the submission to check

    Returns:
        bool: True => submission exists, False => submission does not exist
    """
    response = self.__submissionTable.get_item(
      Key={
        'id': idOfTheSubmission
      }
    )
    try:
      testVar = response["Item"]
      return True
    except KeyError:
      return False

  def fullscanSubmission(self):
    """Scan the entire submission table

    Returns:
        list: list of all submissions in the table
    """
    response = self.__submissionTable.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
      response = self.__submissionTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
      data.extend(response['Items'])
    return data

  def getSubmission(self, idOfTheSubmission: str):
    """Get a submission from the database

    Args:
        idOfTheSubmission (str): id of the submission to get

    Returns:
        dict: dictionary of the submission
    """
    response = self.__submissionTable.get_item(
      Key={
        'id': idOfTheSubmission
      }
    )
    try:
      return response["Item"]
    except KeyError:
      return {"ErrorMessage": "Submission Does not Exist"}

  def addSubmission(self, submissionObjJSON: dict):
    """Add submission to the database

    Args:
        submissionObjJSON (dict): dictionary of the submission to add

    Returns:
        _type_: response
    """
    if not self.__exists(submissionObjJSON['id']):
      response = self.__submissionTable.put_item(
        Item=submissionObjJSON
      )
    else:
      response = {
        "ErrorMessage": "Submission already exists"
      }
    return response

  def updateSubmission(self, submissionObjJSON):
    """Update a submission in the database

    Args:
        submissionObjJSON (dict): dictionary of the submission to update

    Returns:
        _type_: response
    """
    if not self.__exists(submissionObjJSON["id"]):
      return {"ErrorMessage": "Submission Does not Exist"}

    response = self.__submissionTable.update_item(
      Key={
        'id': submissionObjJSON["id"]
      },
      UpdateExpression="set #sid=:si, #cid=:ci, #sc=:sc, #gb=:gb, #gd=:gd, #fb=:fb, #pid=:pi",
      ExpressionAttributeValues={
        ':si': submissionObjJSON["studentId"],
        ':ci': submissionObjJSON["challengeId"],
        ':sc': submissionObjJSON["score"],
        ':gb': submissionObjJSON["gradedBy"],
        ':gd': submissionObjJSON["gradedDate"],
        ':fb': submissionObjJSON.get("feedback"),
        ':pi': submissionObjJSON.get("projectId"),
      },
      ExpressionAttributeNames={
        "#sid": "studentId",
        "#cid": "challengeId",
        "#sc": "score",
        "#gb": "gradedBy",
        "#gd": "gradedDate",
        "#fb": "feedback",
        "#pid": "projectId"
      },
      ReturnValues="UPDATED_NEW"
    )
    return response

  def deleteSubmission(self, idOfTheSubmission: str):
    """Delete a submission from the database

    Args:
        idOfTheSubmission (str): id of the submission to delete

    Returns:
        _type_: response
    """
    response = self.__submissionTable.delete_item(
      Key={
        'id': idOfTheSubmission
      }
    )
    return response
