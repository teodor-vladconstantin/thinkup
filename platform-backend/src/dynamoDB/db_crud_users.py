from boto3.dynamodb.conditions import Attr


class DB_CRUD_USERS:
    def __init__(self, userTable):
        """Initialize the DB_CRUD_USERS class

        Args:
            userTable (_type_): reference to the user table
        """
        self.__userTable = userTable

    def __exists(self, idOfTheUser):
        """Check if the user exists in the database

        Args:
            idOfTheUser (str): id of the user to check

        Returns:
            bool: True => user exists, False => user does not exist
        """
        response = self.__userTable.get_item(
            Key={
                'id': idOfTheUser
            }
        )
        try:
            testVar = response["Item"]
            return True
        except KeyError:
            return False

    def getAllUsers(self):
        """Return all users sorted by name from the database

        Returns:
            list: list containing id, name, profile picture, profile picture extension and the role of the students
        """
        response = self.__userTable.scan(AttributesToGet=['id', 'name', 'profile_picture', 'profile_picture_extension', 'role'])
        sorted(response, key=lambda x:x[1])
        return response

    def searchUser(self, username: str):
        """Search for all the users that match the username

        Args:
            username (str): username to search for

        Returns:
            list: list of all matching users
        """
        response = self.__userTable.scan(FilterExpression=Attr('search_term').contains(username.lower()))
        data = [{"name": x["name"], "profile_picture": x["profile_picture"], "profile_picture_extension": x["profile_picture_extension"], "role": x["role"]} for x in response["Items"]]
        return data

    def getUser(self, idOfTheUser):
        """Get details of an user from the database

        Args:
            idOfTheUser (str): id of the user

        Returns:
            dict: dictionary of the user
        """
        response = self.__userTable.get_item(
            Key={
                'id': idOfTheUser
            }
        )
        try:
            return response["Item"]
        except KeyError:
            return {"ErrorMessage": "User Does not Exist"}

    def addUser(self, userObjJSON):  # + Check existance
        """Add an user to the database

        Args:
            userObjJSON (dict): user dictionary

        Returns:
            _type_: response
        """
        response = self.__userTable.put_item(
            Item=userObjJSON
        )
        return response

    def updateUser(self, userJSONobj):
        """Update an user in the database

        Args:
            userJSONobj (dict): dictionary of the user

        Returns:
            _type_: response
        """
        if not self.__exists(userJSONobj["id"]):
            return {"ErrorMessage": "User Does not Exist"}
        response = self.__userTable.update_item(
            Key={
                'id': userJSONobj["id"]
            },
            UpdateExpression="set #nm=:n, #stm=:sht, #stgs=:s, #dsc=:d, #pfp=:p, #pfpe=:pe, #cvp=:c, #cvpe=:ce, #act=:a, #pzl=:z, #pobj=:po, #scnt=:sc, #fvfl=:ff",
            ExpressionAttributeValues={
                ':n': userJSONobj["name"],
                ':sht': userJSONobj["search_term"],
                ':d': userJSONobj["description"],
                ':p': userJSONobj["profile_picture"],
                ':pe': userJSONobj["profile_picture_extension"],
                ':c': userJSONobj['cover_picture'],
                ':ce': userJSONobj['cover_picture_extension'],
                ':s': userJSONobj["settings"],
                ':a': userJSONobj["activity"],
                ':z': userJSONobj["puzzle"],
                ':po': userJSONobj["personal_objectives"],
                ':sc': userJSONobj["social_connections"],
                ':ff': userJSONobj["fav_files"]
            },
            ExpressionAttributeNames={
                "#nm": "name",
                "#stm": "search_term",
                "#dsc": "description",
                "#pfp": "profile_picture",
                "#pfpe": "profile_picture_extension",
                "#cvp": "cover_picture",
                "#cvpe": "cover_picture_extension",
                "#stgs": "settings",
                "#act": "activity",
                "#pzl": "puzzle",
                "#pobj": "personal_objectives",
                "#scnt": "social_connections",
                "#fvfl": "fav_files"

            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def deleteUser(self, idOfTheUser: str):
        """Delete an user from the database

        Args:
            idOfTheUser (str): id of the user

        Returns:
            _type_: response
        """
        response = self.__userTable.delete_item(
        Key = {
            'id': idOfTheUser
        }
        )
        return response
