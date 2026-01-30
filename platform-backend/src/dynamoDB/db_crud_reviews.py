class DB_CRUD_REVIEWS:
    def __init__(self, reviewTable):
        self.__reviewTable = reviewTable

    def __exists(self, idOfTheReward):
        response = self.__reviewTable.get_item(
            Key = {
                'id': idOfTheReward
            }
        )
        try:
            testVar = response["Item"]
            return True
        except KeyError:
            return False

    def getReview(self, idOfTheReward):
        response = self.__reviewTable.get_item(
            Key = {
                'id': idOfTheReward
            }
        )
        try:
            return response["Item"]
        except KeyError:
            return {"Error Message": "Review does not exist"}

    def addReview(self, reviewObjJson):  # + Check existance
        response = self.__reviewTable.put_item(
            Item=reviewObjJson
        )
        return response

    def updateReview(self, reviewObjJson):
        if not self.__exists(reviewObjJson['id']):
            return {"Error message": "Review does not exist"}

        response = self.__reviewTable.update_item(
            Key={
                'id': reviewObjJson['id']
            },
            UpdateExpression = "set #uid=:#u #rvd=:#d #rvr=:#r",
            ExpressionAttributes = {
                ':u': reviewObjJson['userID'],
                ':d': reviewObjJson['review_description'],
                ':r': reviewObjJson['review_rating']
            },
            ExpressionAttributeNames = {
                "#uid": "userID",
                "#rvd": "review_description",
                "#rvr": "review_rating"
            },
            ReturnValue="UPDATED_NEW"
        )
        return response

    def deleteReview(self, idOfTheReview):
        response = self.__reviewTable.delete_item(
            Key={
                'id': idOfTheReview
            }
        )
        return response
