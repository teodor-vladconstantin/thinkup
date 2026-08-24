class DB_CRUD_MENTOR_TOKENS():
    def __init__(self, mentorTokenTable):
            """
            Initialize the DB_CRUD_MENTOR_TOKENS class

            Args:
                mentorTokenTable (_type_): reference to the mentor token table
            """
            self.__mentorTokenTable = mentorTokenTable
    def deleteToken(self, token: str):
        
        """Delete a token from db

        Args:
            token (str): token to delete
        
        Returns:
            _type_: response
        """
        response = self.__mentorTokenTable.delete_item(
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
        response = self.__mentorTokenTable.get_item(
        Key={
            'token': token
        }
        )
        try:
            temp = response["Item"]
            return True
        except KeyError:
            return False