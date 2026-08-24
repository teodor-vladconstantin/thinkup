class DB_CRUD_GOALS:
    def __init__(self, goalTable):
        """Initialize the DB_CRUD_GOALS class

        Args:
            goalTable (_type_): reference to the goals table
        """
        self.__goalTable = goalTable

    def __exists(self, idOfTheGoal: str):
        """Check if the goal exists in the database

        Args:
            idOfTheGoal (str): id of the goal

        Returns:
            _type_: True => exists, False => does not exist
        """
        response = self.__goalTable.get_item(
            Key={
                'id': idOfTheGoal
            }
        )
        try:
            testVar = response["Item"]
            return True
        except KeyError:
            return False

    def getGoal(self, idOfTheGoal: str):  # Done
        """Get a goal from the database

        Args:
            idOfTheGoal (str): id of the goal

        Returns:
            JSON: JSON of the goal
        """
        response = self.__goalTable.get_item(
            Key={
                'id': idOfTheGoal
            }
        )
        try:
            return response["Item"]
        except KeyError:
            return {"ErrorMessage": "Goal Does not Exist"}

    def addGoal(self, goalObjJSON: dict):
        """Adds a goal to the database

        Args:
            goalObjJSON (dict): JSON Encoded version of the goal object 

        Returns:
            _type_: response
        """
        response = self.__goalTable.put_item(
            Item=goalObjJSON
        )
        return response

    def updateGoal(self, goalObjJSON: dict):
        """Update a goal

        Args:
            goalObjJSON (dict): JSON Encoded version of the goal object

        Returns:
            _type_: resposnse
        """

        response = self.__goalTable.update_item(
            Key={
                'id': goalObjJSON["id"]
            },
            UpdateExpression="set #nm=:n, #dscp=:d, #stp=:s, #deadl=:l", 
            ExpressionAttributeValues={
                ':n': goalObjJSON["name"],
                ':d': goalObjJSON["description"],
                ':s': goalObjJSON["state"],
                ':l': goalObjJSON["deadline"],
            },
            ExpressionAttributeNames={
                "#nm": "name",
                "#dscp": "description", 
                "#stp": "state",
                "#deadl": "deadline",
            },
            ReturnValues="UPDATED_NEW"
        )
        print("RESPONSE : ")
        print(response)
        return response

    def deleteGoal(self, idOfTheGoal: str):
        """Delete a goal from the database

        Args:
            idOfTheGoal (str): id of the goal to be deleted

        Returns:
            _type_: response
        """
        response = self.__goalTable.delete_item(
            Key={
                'id': idOfTheGoal
            }
        )
        return response
