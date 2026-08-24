import boto3
from dynamoDB import setup
from flask import send_file
from s3 import S3setup
from s3.s3_crud import S3_OPERATIONS

dbOpenSchool = setup.startSetup('S3-IDs-OpenSchool')

class OPEN_SCHOOL:
  def __init__(self, bucket):
    self.__bucket = bucket
    self.__s3 = S3_OPERATIONS('thinkup-open-school')
    
  def addFile(self, file, filename):
    return self.__s3.Upload(filename, file, True)

  def downloadFile(self, fileName):
    # self.__s3 = S3setup.startSetup('client') # Removed direct client usage to use abstracted S3_OPERATIONS if slightly modified, 
    # BUT existing code calls boto3 client directly here.
    # We must intercept this call or modify it to use S3_OPERATIONS download mechanism which is mocked.
    # The original code was: 
    # self.__s3 = S3setup.startSetup('client')
    # file = self.__s3.get_object(Bucket=self.__bucket, Key=fileName)
    
    # We will redirect to invoke our S3_OPERATIONS wrapper which handles local switch
    # NOTE: fileName includes extension in this context usually? Let's check usages.
    # Actually, S3_OPERATIONS.Download takes (id, extension).
    # This downloadFile takes fileName.
    # We need to adapt.
    
    import os
    STORAGE_MODE = os.getenv('STORAGE_MODE', 's3')
    
    if STORAGE_MODE == 'local':
        # Need to reconstruct where S3_OPERATIONS would look
        local_path = os.path.join(os.getcwd(), 'local_storage', self.__bucket, fileName)
        if os.path.exists(local_path):
             return {
                'Body': open(local_path, 'rb'),
                'ContentType': 'application/octet-stream'
            }
        raise FileNotFoundError("Local file not found")

    self.__s3 = S3setup.startSetup('client')
    file = self.__s3.get_object(Bucket=self.__bucket, Key=fileName)
    return file
    
    return send_file(
      file['Body'],
      as_attachment=True,
      attachment_filename=fileName,
      mimetype='text/plain',
    )

  def getByOrder(self, order):
    
    # Local FS override
    import os
    from config import STORAGE_MODE
    
    if os.environ.get('STORAGE_MODE') == 'local':
        local_dir = os.path.join(os.getcwd(), 'local_storage', 'thinkup-open-school')
        all_objects = []
        if os.path.exists(local_dir):
            for f in os.listdir(local_dir):
                 full_path = os.path.join(local_dir, f)
                 ts = os.path.getmtime(full_path)
                 from datetime import datetime
                 dt = datetime.fromtimestamp(ts)
                 # Mock structure of s3 response
                 all_objects.append((dt, f))
    else:
        # Original S3 logic
        s3_client = S3setup.startSetup('client')
    
        all_objects = []
        kwargs = {'Bucket': 'thinkup-open-school'}
    
        while True:
          response = s3_client.list_objects_v2(**kwargs)
    
          for object in response.get('Contents', []): # Safety fix
            all_objects.append((object['LastModified'], object['Key']))
    
          try:
              # Next page
              kwargs['ContinuationToken'] = response['NextContinuationToken']
          except KeyError:
              break

    if order == 'desc':
      sorted_keys = [object[1] for object in sorted(all_objects, reverse=True)]
    else:
      sorted_keys = [object[1] for object in sorted(all_objects)]

    sorted_extended = []

    for key in sorted_keys:
      key = key.split('.')[0]
      sorted_extended.append(dbOpenSchool.getDetails( key))

    return {'sorted': [sorted_extended]}

  def deleteFile(self, fileId, fileJson):
    s32 = S3setup.startSetup('resource')
    filename = fileId
    obj = s32.Object(self.__bucket, filename)
    return obj.delete()




    
  
