import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Force local settings for verification
endpoint_url = os.getenv('DYNAMODB_ENDPOINT_URL', 'http://127.0.0.1:8000')
region = os.getenv('REGION_NAME', 'us-east-1')

print(f"VERIFICARE CONEXIUNE:")
print(f"---------------------")
print(f"1. Endpoint URL: {endpoint_url} (Acesta este adresa locala ScyllaDB/Moto, nu AWS)")
print(f"2. Region:       {region}")

try:
    client = boto3.client(
        'dynamodb',
        endpoint_url=endpoint_url,
        region_name=region,
        aws_access_key_id='local',
        aws_secret_access_key='local'
    )
    
    print("\n3. Incercare conectare...")
    tables = client.list_tables()
    print(f"   SUCCES! Conectat la baza de date LOCALA.")
    print(f"   Tabele gasite in ScyllaDB local:")
    for table in tables['TableNames']:
        print(f"    - {table}")
        
except Exception as e:
    print(f"   ESEC: Nu s-a putut conecta la {endpoint_url}")
    print(f"   Eroare: {e}")
