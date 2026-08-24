import boto3
import os
from dotenv import load_dotenv

load_dotenv()

S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', 'http://127.0.0.1:9000')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'local')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'localpassword')
REGION_NAME = os.getenv('REGION_NAME', 'us-east-1')

buckets = [
    'thinkup-profile-picture',
    'thinkup-user-cover-images',
    'thinkup-open-school',
    'thinkup-thumbnail',
    'thinkup-files',
    'thinkup-logos'
]

def init_s3():
    print(f"Connecting to S3 at {S3_ENDPOINT_URL}...")
    s3 = boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    )

    for bucket in buckets:
        try:
            s3.create_bucket(Bucket=bucket)
            print(f"Bucket created: {bucket}")
        except Exception as e:
            if "BucketAlreadyOwnedByYou" in str(e) or "BucketAlreadyExists" in str(e):
                print(f"Bucket already exists: {bucket}")
            else:
                print(f"Error creating bucket {bucket}: {e}")

    # Set bucket policy to public read (simulating typical public S3 bucket for assets)
    # Note: MinIO policies might differ slightly, but let's try basic config if needed.
    # For now, let's assume private or standard ACLs work for the app logic.
    
if __name__ == "__main__":
    init_s3()
