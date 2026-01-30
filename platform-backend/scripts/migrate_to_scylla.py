import boto3
import os
import sys
from decimal import Decimal
from tqdm import tqdm
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Add parent directory to path to allow importing from src if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# Configuration
# Source: AWS (Real) or another endpoint
SOURCE_REGION = os.getenv('AWS_REGION', 'eu-central-1') 
SOURCE_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID_SOURCE') # Special env var for source if needed
SOURCE_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY_SOURCE')

# Destination: ScyllaDB (Local)
DEST_ENDPOINT = os.getenv('DYNAMODB_ENDPOINT_URL', 'http://127.0.0.1:8000')
DEST_REGION = os.getenv('REGION_NAME', 'us-east-1')
DEST_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', 'local')
DEST_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'local')

TABLES_TO_MIGRATE = [
    "Users", "Goals", "S3-IDs", "Materials", "S3-IDs-OpenSchool", 
    "Personal-Objectives", "Project-Tokens", "Mentor-Tokens", 
    "Reviews", "Mentor-Feedback", "Projects"
]

def get_source_resource():
    """Connect to Source DynamoDB (usually AWS)"""
    # If source keys are not explicitly set, fall back to default or error out
    # For this script we assume the user might provide them via env
    if SOURCE_ACCESS_KEY and SOURCE_SECRET_KEY:
        return boto3.resource(
            'dynamodb',
            region_name=SOURCE_REGION,
            aws_access_key_id=SOURCE_ACCESS_KEY,
            aws_secret_access_key=SOURCE_SECRET_KEY
        )
    else:
        # Fallback to default credentials (e.g. AWS CLI profile)
        print("Using default AWS profile for SOURCE")
        return boto3.resource('dynamodb', region_name=SOURCE_REGION)

def get_dest_resource():
    """Connect to Destination ScyllaDB"""
    return boto3.resource(
        'dynamodb',
        endpoint_url=DEST_ENDPOINT,
        region_name=DEST_REGION,
        aws_access_key_id=DEST_ACCESS_KEY,
        aws_secret_access_key=DEST_SECRET_KEY,
        aws_session_token=None  # Ensure we don't accidentally use source session tokens
    )

def convert_decimals(obj):
    """Helper to handle Decimal types from DynamoDB"""
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 else int(obj)
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    return obj

def create_table_if_not_exists(table_name, source_db, dest_db):
    try:
        dest_db.meta.client.describe_table(TableName=table_name)
        print(f"  Table {table_name} already exists in destination.")
        return
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceNotFoundException':
            print(f"  Error checking table existence: {e}")
            return

    print(f"  Creating table {table_name} in destination...")
    try:
        src_table = source_db.Table(table_name)
        # Force load schema
        src_table.load()
        
        params = {
            'TableName': table_name,
            'KeySchema': src_table.key_schema,
            'AttributeDefinitions': src_table.attribute_definitions,
            'BillingMode': 'PAY_PER_REQUEST'
        }

        if src_table.global_secondary_indexes:
            gsis = []
            for gsi in src_table.global_secondary_indexes:
                gsis.append({
                    'IndexName': gsi['IndexName'],
                    'KeySchema': gsi['KeySchema'],
                    'Projection': gsi['Projection']
                })
            params['GlobalSecondaryIndexes'] = gsis
            
        if src_table.local_secondary_indexes:
            lsis = []
            for lsi in src_table.local_secondary_indexes:
                lsis.append({
                    'IndexName': lsi['IndexName'],
                    'KeySchema': lsi['KeySchema'],
                    'Projection': lsi['Projection']
                })
            params['LocalSecondaryIndexes'] = lsis

        dest_db.create_table(**params)
        print(f"  Table {table_name} created successfully.")
        
    except Exception as e:
        print(f"  Error creating table {table_name}: {e}")

def migrate_table(table_name, source_db, dest_db):
    print(f"\nMigrating table: {table_name}")
    
    # 0. Ensure table exists
    create_table_if_not_exists(table_name, source_db, dest_db)

    src_table = source_db.Table(table_name)
    dst_table = dest_db.Table(table_name)
    
    # 1. Scan source
    try:
        response = src_table.scan()
        items = response['Items']
        
        while 'LastEvaluatedKey' in response:
            response = src_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
            
        print(f"  Found {len(items)} items in source.")
    except Exception as e:
        print(f"  Error scanning source table {table_name}: {e}")
        return

    if not items:
        return

    # 2. Write to destination
    success_count = 0
    # Add small delay to ensure table is active if just created
    import time
    time.sleep(2)
    
    with dst_table.batch_writer() as batch:
        for item in tqdm(items, desc=f"  Writing to {table_name}", unit="item"):
            try:
                # Write item directly
                batch.put_item(Item=item)
                success_count += 1
            except ClientError as e:
                print(f"  Error writing item: {e}")

    print(f"  Successfully migrated {success_count}/{len(items)} items.")

def main():
    print("=== STARTING MIGRATION: AWS -> SCYLLA DB ===")
    print(f"Source Region: {SOURCE_REGION}")
    print(f"Destination: {DEST_ENDPOINT}")
    
    source_db = get_source_resource()
    dest_db = get_dest_resource()
    
    # Optional: Check connection
    try:
        list(dest_db.tables.all())
        print("Connected to Destination ScyllaDB ✅")
    except Exception as e:
        print(f"Failed to connect to Destination: {e}")
        return

    for table in TABLES_TO_MIGRATE:
        migrate_table(table, source_db, dest_db)
        
    print("\n=== MIGRATION COMPLETE ===")

if __name__ == "__main__":
    main()
