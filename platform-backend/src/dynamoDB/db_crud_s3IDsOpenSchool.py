from boto3.dynamodb.conditions import Attr, Key


class DB_CRUD_S3IDS_OPENSCHOOL:
  def __init__(self, openSchoolTable) :
    self.__openSchoolTable = openSchoolTable

  def addId (self, ObjJson):
    response = self.__openSchoolTable.put_item(
      Item = ObjJson
    )

  def getDetails(self, idOfTheFile):
    response = self.__openSchoolTable.get_item(
      Key = {
        'id': idOfTheFile
      }
    )
    try:
      return response["Item"]
    except KeyError:
      return {"ErrorMessage": "File Does not Exist"}

  def deleteId(self, idToDelete):
    response = self.__openSchoolTable.delete_item(
      Key={
        'id': idToDelete
      }
    )
    return response

  def searchForFileThatStartWith(self, prefix, attr):
    response = self.__openSchoolTable.scan(FilterExpression=Attr(attr).contains(prefix.lower()))
    return response['Items']

  def updateId(self, idJson: dict):
    response = self.__openSchoolTable.update_item(
      Key={
                'id': idJson["id"]
            },
            UpdateExpression="set #tw=:v", 
            ExpressionAttributeValues={
                ':v': idJson["total_views"],
            },
            ExpressionAttributeNames={
                "#tw": "total_views",
            },
            ReturnValues="UPDATED_NEW"
    )
    return response
