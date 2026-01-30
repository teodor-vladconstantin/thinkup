import boto3
import os
from dotenv import load_dotenv

load_dotenv()

DYNAMODB_ENDPOINT_URL = os.getenv('DYNAMODB_ENDPOINT_URL', 'http://127.0.0.1:8000')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'local')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'local')
REGION_NAME = os.getenv('REGION_NAME', 'us-east-1')

def add_demo_token():
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME,
            endpoint_url=DYNAMODB_ENDPOINT_URL
        )
        
        table = dynamodb.Table('Project-Tokens')
        
        token = "TOKEN_demo3efv"
        
        print(f"Adding token {token} to Project-Tokens table...")
        
        response = table.put_item(
            Item={
                'token': token
            }
        )
        
        print("Token added successfully.")
        
    except Exception as e:
        print(f"Error adding token: {e}")

if __name__ == "__main__":
    add_demo_token()