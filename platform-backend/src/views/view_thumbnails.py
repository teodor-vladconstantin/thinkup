from api.api_crud_thumbnails import API_CRUD_THUMBNAILS
from dynamoDB import setup
from flask import Blueprint, request
from s3.s3_crud import S3_OPERATIONS

urlThumbnails = Blueprint('views', __name__)

apiThumbnails = API_CRUD_THUMBNAILS()

@urlThumbnails.route('/thumbnails/<string:id>', methods=['GET'])
def getThumbnail(idOfThumbnail: str):
  """Get a thumbnail from database

  Args:
      idOfThumbnail (str): id of the thumbnail

  Returns:
      dict: dicitonary of the thumbnail
  """
  return apiThumbnails.getThumbnail(idOfThumbnail)
