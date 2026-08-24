import boto3
import json
import os
import decimal
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

# Config
DEST_ENDPOINT = os.getenv('DYNAMODB_ENDPOINT_URL', 'http://127.0.0.1:8000')
DEST_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', 'local')
DEST_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'local')
DEST_REGION = os.getenv('REGION_NAME', 'us-east-1')

TABLES = [
    "Users", "Goals", "S3-IDs", "Materials", "S3-IDs-OpenSchool", 
    "Personal-Objectives", "Project-Tokens", "Mentor-Tokens", 
    "Reviews", "Mentor-Feedback", "Projects"
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'seed_data')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    print(f"Connecting to Scylla at {DEST_ENDPOINT}...")
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=DEST_ACCESS_KEY,
        aws_secret_access_key=DEST_SECRET_KEY,
        region_name=DEST_REGION,
        endpoint_url=DEST_ENDPOINT
    )

    print(f"Dumping tables to {DATA_DIR}...")
    
    for table_name in TABLES:
        try:
            table = dynamodb.Table(table_name)
            response = table.scan()
            data = response['Items']
            
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                data.extend(response['Items'])
            
            file_path = os.path.join(DATA_DIR, f"{table_name}.json")
            with open(file_path, 'w') as f:
                json.dump(data, f, cls=DecimalEncoder, indent=2)
                
            print(f"✓ {table_name}: {len(data)} items saved.")
            
        except Exception as e:
            print(f"✗ {table_name}: Error - {str(e)}")

if __name__ == '__main__':
    main()
