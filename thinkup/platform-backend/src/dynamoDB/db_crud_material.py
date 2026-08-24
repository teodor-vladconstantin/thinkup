import json


class DB_CRUD_MATERIAL:
    def __init__(self, materialTable):
        """Initialize the DB_CRUD_MATERIAL class

        Args:
            materialTable (_type_): reference to the materials table
        """
        self.__materialTable = materialTable

    def __exists(self, idOfTheMaterial: str):
        """Check if the material exists in the database

        Args:
            idOfTheMaterial (str): id of the material

        Returns:
            _type_: True => exists, False => does not exist
        """
        response = self.__materialTable.get_item(
            Key={
                'id': idOfTheMaterial
            }
        )

        try:
            testVar = response["Item"]
            return True
        except KeyError:
            return False

    def fullScanMaterial(self):
        """FullScan the materials table

        Returns:
            _type_: _description_
        """
        response = self.__materialTable.scan()
        data = response["Items"]

        while 'LastEvaluatedKey' in response:
            response = self.__materialTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response["Items"])

        return data

    def getMaterial(self, idOfTheMaterial: str):
        """Get a material from the database

        Args:
            idOfTheMaterial (str): id of the material

        Returns:
            JSON: JSON of the material
        """
        response = self.__materialTable.get_item(
            Key={
                'id': idOfTheMaterial
            }
        )

        try:
            # print(json.dumps(response["Item"]), type(json.dumps(response["Item"])))
            return json.dumps(response["Item"])
        except KeyError:
            return {"ErrorMessage": "Material does not exist!"}

    def addMaterial(self, materialJson: dict):
        """Add material to the database

        Args:
            materialJson (dict): JSON Encoded version of the material object

        Returns:
            _type_: response
        """
        response = self.__materialTable.put_item(
            Item=materialJson
        )

        return response

    def updateMaterial(self, materialId:str, materialJson: dict):
        """Update a material in the database

        Args:
            materialId (str): the id of the project to be updated
            materialJson (dict): JSON Encoded version of the material object

        Returns:
            _type_: response
        """
        if self.__exists(materialId) is False:
            return {"ErrorMessage": "Material does not exist!"}

        response = self.__materialTable.update_item(

            Key={
                'id': materialId
            },

            UpdateExpression="set #nm=:n, #dsc=:d, #lfls=:f",

            ExpressionAttributeValues={
                ':n': materialJson["name"],
                ':d': materialJson["description"],
                ':f': materialJson["files"]
            },
            ExpressionAttributeNames={
                "#nm": "name",
                "#dsc": "description",
                "#lfls": "files"
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def deleteMaterial(self, idOfTheMaterial: str):
        """Delete a material from database

        Args:
            idOfTheMaterial (str): id of the material

        Returns:
            _type_: response
        """
        response = self.__materialTable.delete_item(
            Key={
                'id': idOfTheMaterial
            }
        )
        return response
