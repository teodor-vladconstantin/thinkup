class DB_CRUD_PROJECT_TOKENS:
  def __init__(self, tokenTable):
    """Initialize the DB_CRUD_PROJECT_TOKENS class
    
    Args:
        tokenTable (_type_): reference to the token table
    """
    self.__tokenTable = tokenTable

  def deleteToken(self, token: str):
    """Delete a token from db

    Args:
        token (str): token to delete
    
    Returns:
        _type_: response
    """
    response = self.__tokenTable.delete_item(
      Key={
        'token': token
      }
    )
    return response


  def isTokenValid(self, token: str):
    """Check if a token is valid
    
    Args:
        token (str): token to check
    
    Returns:
        bool: True if the token is valid, False otherwise
    """
    response = self.__tokenTable.get_item(
      Key={
        'token': token
      }
    )
    try:
      temp = response["Item"]
      return True
    except KeyError:
      return False
