from boto3.dynamodb.conditions import Attr


class DB_CRUD_CHALLENGES:
  def __init__(self, challengeTable):
    """Initialize DB_CRUD_CHALLENGES class

    Args:
        challengeTable (_type_): db reference to the challenge table
    """
    self.__challengeTable = challengeTable

  def __exists(self, idOfTheChallenge: str):
    """Check if the challenge exists in the database

    Args:
        idOfTheChallenge (str): id of the challenge to check

    Returns:
        bool: True => challenge exists, False => challenge does not exist
    """
    response = self.__challengeTable.get_item(
      Key={
        'id': idOfTheChallenge
      }
    )
    try:
      testVar = response["Item"]
      return True
    except KeyError:
      return False

  def fullscanChallenge(self):
    """Scan the entire challenge table

    Returns:
        list: list of all challenges in the table
    """
    response = self.__challengeTable.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
      response = self.__challengeTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
      data.extend(response['Items'])
    return data

  def getChallenge(self, idOfTheChallenge: str):
    """Get a challenge from the database

    Args:
        idOfTheChallenge (str): id of the challenge to get

    Returns:
        dict: dictionary of the challenge
    """
    response = self.__challengeTable.get_item(
      Key={
        'id': idOfTheChallenge
      }
    )
    try:
      return response["Item"]
    except KeyError:
      return {"ErrorMessage": "Challenge Does not Exist"}

  def addChallenge(self, challengeObjJSON: dict):
    """Add challenge to the database

    Args:
        challengeObjJSON (dict): dictionary of the challenge to add

    Returns:
        _type_: response
    """
    if not self.__exists(challengeObjJSON['id']):
      response = self.__challengeTable.put_item(
        Item=challengeObjJSON
      )
    else:
      response = {
        "ErrorMessage": "Challenge already exists"
      }
    return response

  def updateChallenge(self, challengeObjJSON):
    """Update a challenge in the database

    Args:
        challengeObjJSON (dict): dictionary of the challenge to update

    Returns:
        _type_: response
    """
    if not self.__exists(challengeObjJSON["id"]):
      return {"ErrorMessage": "Challenge Does not Exist"}

    response = self.__challengeTable.update_item(
      Key={
        'id': challengeObjJSON["id"]
      },
      UpdateExpression="set #nm=:n, #dscp=:d, #dl=:dl, #ms=:ms, #crtby=:c, #crd=:cd",
      ExpressionAttributeValues={
        ':n': challengeObjJSON["name"],
        ':d': challengeObjJSON["description"],
        ':dl': challengeObjJSON["deadline"],
        ':ms': challengeObjJSON["maxScore"],
        ':c': challengeObjJSON["createdBy"],
        ':cd': challengeObjJSON["creationDate"],
      },
      ExpressionAttributeNames={
        "#nm": "name",
        "#dscp": "description",
        "#dl": "deadline",
        "#ms": "maxScore",
        "#crtby": "createdBy",
        "#crd": "creationDate"
      },
      ReturnValues="UPDATED_NEW"
    )
    return response

  def deleteChallenge(self, idOfTheChallenge: str):
    """Delete a challenge from the database

    Args:
        idOfTheChallenge (str): id of the challenge to delete

    Returns:
        _type_: response
    """
    response = self.__challengeTable.delete_item(
      Key={
        'id': idOfTheChallenge
      }
    )
    return response
