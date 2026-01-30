from boto3.dynamodb.conditions import Attr, Key


class DB_CRUD_PERSONAL_OBJECTIVES:
  def __init__(self, objectiveTable):
    """Initialize the DB_CRUD_PERSONAL_OBJECTIVES class

    Args:
        objectiveTable (_type_): reference to the objectives table
    """
    self.__objectiveTable = objectiveTable

  def getObjective(self, idOfTheObjective: str):
    """Get an objective from the database

    Args:
        idOfTheObjective (str): id of the objective

    Returns:
        dict: dictionary of the objective
    """
    response = self.__objectiveTable.get_item(
      Key={
        'id': idOfTheObjective
      }
    )
    try:
      return response["Item"]
    except KeyError:
      return {"ErrorMessage": "Objective Does not Exist"}

  def addObjective(self, objective: dict):
    """Add an objective to the database

    Args:
        objective (dict): dictionary of the objective

    Returns:
        _type_: response
    """
    response = self.__objectiveTable.put_item(
      Item=objective
    )
    return response

  def deleteObjective(self, idOfTheObjective: str):
    """Delete an objective from the database

    Args:
        idOfTheObjective (str): id of the objective

    Returns:
        _type_: response
    """
    response = self.__objectiveTable.delete_item(
      Key={
        'id': idOfTheObjective
      }
    )
    return response

  def updateObjective(self, poJSON: dict):
    """Update an objective in the database

    Args:
        poJSON (dict): dictionary of the objective

    Returns:
        _type_: response
    """
    response = self.__objectiveTable.update_item(
    Key={
      'id': poJSON["id"]
    },
    UpdateExpression="set #nm=:n, #dscp=:d, #stp=:s, #deadl=:l", 
    ExpressionAttributeValues={
      ':n': poJSON["name"],
      ':d': poJSON["description"],
      ':s': poJSON["state"],
      ':l': poJSON["deadline"],
    },
    ExpressionAttributeNames={
        "#nm": "name",
        "#dscp": "description", 
        "#stp": "state",
        "#deadl": "deadline",
    },
    ReturnValues="UPDATED_NEW"
    )
    return response

