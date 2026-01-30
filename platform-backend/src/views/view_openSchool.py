import os

import boto3
from dynamoDB import setup
from flask import Blueprint, request
from model.entity.jsonencoders.idOpenSchool_encoder import IdOpenSchoolEncoder
from model.entity.open_school.open_school import OPEN_SCHOOL

urlOpenSchool = Blueprint('openSchool', __name__)

S3openSchool = OPEN_SCHOOL('thinkup-open-school')
dbOpenSchool = setup.startSetup('S3-IDs-OpenSchool')

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.environ.get('REGION_NAME')
DYNAMODB_ENDPOINT_URL = os.environ.get('DYNAMODB_ENDPOINT_URL')

@urlOpenSchool.route('/openSchool/search/byTime/<string:order>', methods=['GET'])
def getByTime(order):
  # asc -> ascending , desc -> descending
  return S3openSchool.getByOrder(order)

@urlOpenSchool.route('/openSchool/increasePopularity/<string:id>', methods=['PUT'])
def increasePopularity(id):
  fileJson = dbOpenSchool.getDetails(id)
  fileJson['total_views'] += 1
  return dbOpenSchool.updateId(fileJson)

@urlOpenSchool.route('/openSchool', methods=['POST'])
def addFile():
  files = request.files.getlist('files')

  for file in files:

    pathname, extension = os.path.splitext(file.filename)
    # Add file to dynamodb
    dbOpenSchool.addId(IdOpenSchoolEncoder.toJson(pathname, 0, str(pathname).lower(), extension))
    S3openSchool.addFile(file, pathname)
  return "OK"

@urlOpenSchool.route('/openSchool/<string:id>', methods=['DELETE'])
def deleteFile(id):
  fileJson = dbOpenSchool.getDetails(id)
  # Delete from dynamodb
  dbOpenSchool.deleteId(id)

  return S3openSchool.deleteFile(id, fileJson)

@urlOpenSchool.route('/openSchool/search/<string:name>', methods=['GET'])
def searchFile(name):
  data = dbOpenSchool.searchForFileThatStartWith(name, "search_term")
  Item = {
    'file': data
  }
  return Item

@urlOpenSchool.route('/openSchool/search/byFiletype/<string:ft>', methods=['GET'])
def searchFileByFileType(ft):
  data = dbOpenSchool.searchForFileThatStartWith(ft, "extension")
  Item = {
    'file': data
  }
  return Item

def removeGeneralFileTypes(data, extensions):
  remove_ids = []
  for d in data:
    if extensions.count(d["extension"]) > 0:
      remove_ids.append(data.index(d))

  data_mod = []
  for data_i in data:
    if data.index(data_i) not in remove_ids:
      data_mod.append(data_i)

  return data_mod

@urlOpenSchool.route('/openSchool/search/byFiletype/etc', methods=['GET'])
def getTheRestOfTheFiletypes():
  extensions = ['.png', '.jpeg', '.jpg', '.svg', '.gif', '.psd', '.doc',  '.docx', '.pdf', '.mp4', '.mov']
  dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = REGION_NAME,
    endpoint_url = DYNAMODB_ENDPOINT_URL
  )

  table = dynamodb.Table('S3-IDs-OpenSchool')


  response = table.scan()
  data = response['Items']

  while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])
    
  data = removeGeneralFileTypes(data, extensions)
  return {"file": data}

def sortByViews(json):
  try:
    return int(json['total_views'])
  except KeyError:
    return 0

@urlOpenSchool.route('/openSchool/search/mostPopular', methods=['GET'])
def searchFileMostPopular():
  dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = REGION_NAME,
    endpoint_url = DYNAMODB_ENDPOINT_URL
  )

  table = dynamodb.Table('S3-IDs-OpenSchool')


  response = table.scan()
  data = response['Items']

  while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])

  data.sort(key=sortByViews, reverse=True)

  return {'sorted':data}
  

