import boto3
import os
import sys
from tqdm import tqdm
from dotenv import load_dotenv

# Config
BUCKETS = [
    'thinkup-profile-picture',
    'thinkup-user-cover-images',
    'thinkup-open-school',
    'thinkup-thumbnail',
    'thinkup-files',
    'thinkup-logos'
]

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # platform-backend
LOCAL_STORAGE_DIR = os.path.join(BASE_DIR, 'local_storage')

# Auth (Source)
SOURCE_REGION = os.getenv('AWS_REGION', 'eu-central-1') 
SOURCE_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID_SOURCE')
SOURCE_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY_SOURCE')

def main():
    print("=== STARTING S3 -> LOCAL FILE MIGRATION ===")
    print(f"Target Directory: {LOCAL_STORAGE_DIR}")

    if not SOURCE_ACCESS_KEY or not SOURCE_SECRET_KEY:
        print("Error: Missing Source AWS Credentials (AWS_ACCESS_KEY_ID_SOURCE, AWS_SECRET_ACCESS_KEY_SOURCE)")
        return

    s3_client = boto3.client(
        's3',
        region_name=SOURCE_REGION,
        aws_access_key_id=SOURCE_ACCESS_KEY,
        aws_secret_access_key=SOURCE_SECRET_KEY
    )

    if not os.path.exists(LOCAL_STORAGE_DIR):
        os.makedirs(LOCAL_STORAGE_DIR)

    for bucket in BUCKETS:
        print(f"\nProcessing Bucket: {bucket}")
        dest_bucket_dir = os.path.join(LOCAL_STORAGE_DIR, bucket)
        
        if not os.path.exists(dest_bucket_dir):
            os.makedirs(dest_bucket_dir)

        try:
            # List objects
            paginator = s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=bucket)
            
            files = []
            for page in page_iterator:
                if 'Contents' in page:
                    files.extend(page['Contents'])
            
            print(f"  Found {len(files)} files.")
            
            for file_obj in tqdm(files, desc=f"  Downloading from {bucket}", unit="file"):
                key = file_obj['Key']
                local_path = os.path.join(dest_bucket_dir, key)
                
                # Ensure nested directories exist if key has slashes
                local_dir = os.path.dirname(local_path)
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                
                # Download
                s3_client.download_file(bucket, key, local_path)
                
        except Exception as e:
            print(f"  Error processing bucket {bucket}: {e}")

    print("\n=== FILE MIGRATION COMPLETE ===")

if __name__ == "__main__":
    main()
