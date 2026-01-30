import os
import shutil

import boto3
from dotenv import load_dotenv
from model.entity.file.file import File

from . import S3setup

load_dotenv()

# s3 = S3setup.startSetup('resource') # Not needed for local storage logic if we bypass it
region=os.getenv('REGION_NAME')
STORAGE_MODE = os.getenv('STORAGE_MODE', 's3') # 's3' or 'local'
LOCAL_STORAGE_PATH = os.path.join(os.getcwd(), 'local_storage')

class S3_OPERATIONS:
  def __init__(self, Bucket):
    self.__bucket = Bucket
    if STORAGE_MODE == 'local':
        self.__storage_path = os.path.join(LOCAL_STORAGE_PATH, Bucket)
        if not os.path.exists(self.__storage_path):
            os.makedirs(self.__storage_path)

  def Upload(self, fileObj, fileItself, isOpenSchool):
    if STORAGE_MODE == 'local':
        try:
            file_path = os.path.join(self.__storage_path, fileItself.filename)
            fileItself.save(file_path)
            # Reset cursor for consistency if needed, though 'save' usually consumes it
            fileItself.seek(0) 
            return "OK"
        except Exception as err:
            print(f"Local Upload Error: {err}")
            return "FAILED"

    # Legacy S3 Logic
    s3 = S3setup.startSetup('resource')
    if isOpenSchool is False:
      try:
        s3.Bucket(self.__bucket).put_object(Key=fileItself.filename, Body=fileItself)
        return "OK"
      except Exception as err:
        return "FAILED"
    try:
      s3.Bucket(self.__bucket).put_object(Key=fileItself.filename, Body=fileItself)
      return "OK"
    except Exception as err:
      return "Failed"

  def Download(self, idOfTheFile, extension):
    if STORAGE_MODE == 'local':
        # Return a file object or path. Boto3 get_object returns a dict with 'Body' as a stream.
        # We need to mimic that interface or adapt the caller.
        # Looking at usages, callers likely expect a boto3 response object. 
        # But 'OPEN_SCHOOL.downloadFile' calls this too.
        # Let's see how to return a mimic object.
        idOfTheFile = idOfTheFile + extension
        file_path = os.path.join(self.__storage_path, idOfTheFile)
        if os.path.exists(file_path):
            return {
                'Body': open(file_path, 'rb'),
                'ContentType': 'application/octet-stream' # Generic
            }
        raise FileNotFoundError("File not found in local storage")

    s3 = S3setup.startSetup('client')
    idOfTheFile = idOfTheFile + extension
    return s3.get_object(Bucket=self.__bucket, Key=idOfTheFile)

  def Delete(self, idOfPhoto, extension):
    if STORAGE_MODE == 'local':
        idOfPhoto = idOfPhoto + extension
        file_path = os.path.join(self.__storage_path, idOfPhoto)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"ResponseMetadata": {"HTTPStatusCode": 204}}
        return {"ResponseMetadata": {"HTTPStatusCode": 404}}

    s3 = S3setup.startSetup('resource')
    idOfPhoto = idOfPhoto + extension
    obj = s3.Object(self.__bucket, idOfPhoto)
    return obj.delete()
