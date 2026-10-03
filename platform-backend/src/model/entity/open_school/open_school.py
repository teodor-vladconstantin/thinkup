import os

from dynamoDB import setup
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
    return self.__s3.Download(*os.path.splitext(fileName))

  def getByOrder(self, order):
    
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
    return self.__s3.Delete(fileId, fileJson['extension'])
