import os

import boto3
import botocore
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
s3_endpoint_url = os.getenv('S3_ENDPOINT_URL')

def startSetup(clientOrResource):
  if clientOrResource == 'resource':
    s3 = boto3.resource(
      "s3",
      region_name=os.environ.get('REGION_NAME'),
      aws_access_key_id=aws_access_key_id,
      aws_secret_access_key=aws_secret_access_key,
      endpoint_url=s3_endpoint_url
    )
    return s3
  s3 = boto3.client(
      "s3",
      region_name=os.environ.get('REGION_NAME'),
      aws_access_key_id=aws_access_key_id,
      aws_secret_access_key=aws_secret_access_key,
      endpoint_url=s3_endpoint_url
  )
  return s3
