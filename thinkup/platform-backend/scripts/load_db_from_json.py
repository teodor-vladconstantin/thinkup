import boto3
import json
import os
import time

# Configurare conexiune ScyllaDB
# Dacă rulăm din Docker, host-ul este 'scylladb', altfel e 'localhost'
endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL', 'http://127.0.0.1:8000')

print(f"Connecting to ScyllaDB at {endpoint_url}...")
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=endpoint_url,
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

SEED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "seed_data")

def load_data():
    if not os.path.exists(SEED_DIR):
        print(f"Error: Directory {SEED_DIR} not found.")
        return

    print(f"Loading data from {SEED_DIR}...")
    
    files = [f for f in os.listdir(SEED_DIR) if f.endswith('.json')]
    
    for filename in files:
        table_name = filename.replace('.json', '')
        filepath = os.path.join(SEED_DIR, filename)
        
        try:
            table = dynamodb.Table(table_name)
            
            # Verificăm dacă tabelul există (simple check)
            try:
                table.load()
            except Exception as e:
                print(f"Warning: Table {table_name} does not exist or is not reachable. Skipping.")
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                items = json.load(f)
            
            if not items:
                print(f"⚠ {table_name}: No items in JSON to load.")
                continue

            print(f"→ Loading {len(items)} items into {table_name}...")
            
            # Batch writer este mult mai rapid pentru inserturi multiple
            with table.batch_writer() as batch:
                for item in items:
                    batch.put_item(Item=item)
            
            print(f"✓ {table_name}: Success.")
            
        except Exception as e:
            print(f"❌ Error loading {table_name}: {e}")

if __name__ == "__main__":
    load_data()
    print("\nDone! Database seeded successfully.")
