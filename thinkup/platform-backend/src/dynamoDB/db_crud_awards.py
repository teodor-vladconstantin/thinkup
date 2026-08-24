class DB_CRUD_AWARDS:
    def __init__(self, awardTable):
        self.__awardTable = awardTable

    def __exists(self, idOfTheAward):
        response = self.__awardTable.get_item(
            Key = {
                'id': idOfTheAward
            }
        )
        try:
            testVar = response["Item"]
            return True
        except KeyError:
            return False

    def get_award(self, idOfTheAward):
        response = self.__awardTable.get_item(
            Key = {
                'id': idOfTheAward
            }
        )
        try:
            return response["Item"]
        except KeyError:
            return {"Error Message": "Award does not exist"}

    def add_award(self, awardObjJSON):  # + Check existence
        response = self.__awardTable.put_item(
            Item=awardObjJSON
        )
        return response

    def update_award(self, awardObjJSON):
        if not self.__exists(awardObjJSON["id"]):
            return {"Error Message": "Award does not exist"}

        response = self.__awardTable.update_item(
            Key = {
                'id': awardObjJSON["id"]
            },
            UpdateExpression = "set #nm=:n, #dscp=:d, #imgid=:m",
            ExpressionAttributeValues={
                ':n': awardObjJSON["name"],
                ':d': awardObjJSON["description"],
                ':m': awardObjJSON["imageId"]
            },
            ExpressionAttributeNames={
                "#nm": "name",
                "#dscp": "description",
                "#imgid": "imageId"
            },
            ReturnValue="UPDATED_NEW"
        )
        return response

    def delete_award(self, idOfTheAward):
        response = self.__awardTable.delete_item(
            Key={
                'id': idOfTheAward
            }
        )
        return response
