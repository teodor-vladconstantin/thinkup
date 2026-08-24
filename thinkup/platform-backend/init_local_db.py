import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'test')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'test')
REGION_NAME = os.getenv('REGION_NAME', 'us-east-1')
DYNAMODB_ENDPOINT_URL = os.getenv('DYNAMODB_ENDPOINT_URL', 'http://127.0.0.1:8000')

def create_table(dynamodb, table_name, pk_name):
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': pk_name,
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': pk_name,
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Creating table {table_name}...")
        table.wait_until_exists()
        print(f"Table {table_name} created.")
    except Exception as e:
        if "ResourceInUseException" in str(e):
            print(f"Table {table_name} already exists.")
        else:
            print(f"Error creating table {table_name}: {e}")

def main():
    print(f"Connecting to DynamoDB at {DYNAMODB_ENDPOINT_URL}...")
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME,
        endpoint_url=DYNAMODB_ENDPOINT_URL
    )

    tables = {
        "Users": "id",
        "Goals": "id",
        "S3-IDs": "id",
        "Materials": "id",
        "S3-IDs-OpenSchool": "id",
        "Personal-Objectives": "id",
        "Project-Tokens": "token",
        "Mentor-Tokens": "token",
        "Reviews": "id",
        "Mentor-Feedback": "id",
        "Projects": "id"
    }

    for table_name, pk_name in tables.items():
        create_table(dynamodb, table_name, pk_name)

if __name__ == "__main__":
    main()
