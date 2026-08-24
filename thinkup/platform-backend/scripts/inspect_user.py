import boto3
import os
import json
from decimal import Decimal

# Helper to handle Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def main():
    endpoint = os.getenv('DYNAMODB_ENDPOINT_URL', 'http://127.0.0.1:8000')
    print(f"Connecting to {endpoint}")
    
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=endpoint,
        region_name='us-east-1',
        aws_access_key_id='local',
        aws_secret_access_key='local'
    )
    
    table = dynamodb.Table('Users')
    
    # Scan one item
    response = table.scan(Limit=1)
    items = response.get('Items', [])
    
    if items:
        print("User Record Sample:")
        print(json.dumps(items[0], cls=DecimalEncoder, indent=2))
    else:
        print("No users found")

if __name__ == "__main__":
    main()
