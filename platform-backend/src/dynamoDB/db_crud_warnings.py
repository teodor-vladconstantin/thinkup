from boto3.dynamodb.conditions import Attr


class DB_CRUD_WARNINGS:
  def __init__(self, warningTable):
    """Initialize DB_CRUD_WARNINGS class

    Args:
        warningTable (_type_): db reference to the warning table
    """
    self.__warningTable = warningTable

  def __exists(self, idOfTheWarning: str):
    """Check if the warning exists in the database

    Args:
        idOfTheWarning (str): id of the warning to check

    Returns:
        bool: True => warning exists, False => warning does not exist
    """
    response = self.__warningTable.get_item(
      Key={
        'id': idOfTheWarning
      }
    )
    try:
      testVar = response["Item"]
      return True
    except KeyError:
      return False

  def fullscanWarning(self):
    """Scan the entire warning table

    Returns:
        list: list of all warnings in the table
    """
    response = self.__warningTable.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
      response = self.__warningTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
      data.extend(response['Items'])
    return data

  def getWarning(self, idOfTheWarning: str):
    """Get a warning from the database

    Args:
        idOfTheWarning (str): id of the warning to get

    Returns:
        dict: dictionary of the warning
    """
    response = self.__warningTable.get_item(
      Key={
        'id': idOfTheWarning
      }
    )
    try:
      return response["Item"]
    except KeyError:
      return {"ErrorMessage": "Warning Does not Exist"}

  def addWarning(self, warningObjJSON: dict):
    """Add warning to the database

    Args:
        warningObjJSON (dict): dictionary of the warning to add

    Returns:
        _type_: response
    """
    if not self.__exists(warningObjJSON['id']):
      response = self.__warningTable.put_item(
        Item=warningObjJSON
      )
    else:
      response = {
        "ErrorMessage": "Warning already exists"
      }
    return response

  def deleteWarning(self, idOfTheWarning: str):
    """Delete a warning from the database

    Args:
        idOfTheWarning (str): id of the warning to delete

    Returns:
        _type_: response
    """
    response = self.__warningTable.delete_item(
      Key={
        'id': idOfTheWarning
      }
    )
    return response
