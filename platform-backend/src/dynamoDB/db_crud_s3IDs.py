class DB_CRUD_S3IDS:
  def __init__(self, idTable):
    """Initialize the DB_CRUD_S3IDS class

    Args:
        idTable (_type_): reference to the id table
    """
    self.__idTable = idTable

  def addId (self, ObjJson: dict):
    """Add an id to the database

    Args:
        ObjJson (dict): dictionary of the id

    Returns:
        _type_: response
    """
    response = self.__idTable.put_item(
      Item = ObjJson
    )
    return response
  
  def getDetails (self, idOfTheObj: str):
    """Get details of an id from the database

    Args:
        idOfTheObj (str): id of the id :)

    Returns:
        dict: dictionary of the id
    """
    response = self.__idTable.get_item(
      Key = {
        'id': idOfTheObj
      }
    )
    try:
      return response["Item"]
    except KeyError:
      return {"ErrorMessage": "User Does not Exist"}
  
  def delete_id(self, idToDelete: str):
    """Delete an id from the database

    Args:
        idToDelete (str): id of the id

    Returns:
        _type_: response
    """
    response = self.__idTable.delete_item(
      Key={
        'id': idToDelete
      }
    )
    return response
