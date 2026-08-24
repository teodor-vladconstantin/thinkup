from flask import send_file
from s3.s3_crud import S3_OPERATIONS


class API_CRUD_THUMBNAILS:
  def __init__(self):
    """Initialize the API_CRUD_THUMBNAILS class
    """
    self.__s3CrudFiles = S3_OPERATIONS('thinkup-thumbnail')
  
  def getThumbnail(self, idOfTheThumbnail: str):
    """Get a thumbnail from database

    Args:
        idOfTheThumbnail (str): id of the thumbnail

    Returns:
        file: thumbnail file
    """
    thumbnail = self.__s3CrudFiles.Download(idOfTheThumbnail, '.png')
    
    return send_file(
      thumbnail['Body'],
      mimetype='image/png'
    )
