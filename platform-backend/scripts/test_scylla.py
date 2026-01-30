import boto3
import os
import sys
import unittest
from dotenv import load_dotenv
from decimal import Decimal

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

class TestScyllaDBCompat(unittest.TestCase):
    def setUp(self):
        self.endpoint = os.getenv('DYNAMODB_ENDPOINT_URL', 'http://127.0.0.1:8000')
        self.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=self.endpoint,
            region_name=os.getenv('REGION_NAME', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'local'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'local')
        )
        self.table_name = "Projects" # Use an existing table
        self.table = self.dynamodb.Table(self.table_name)

    def test_connection(self):
        """Test basic connectivity"""
        print(f"\nTesting connection to {self.endpoint}...")
        try:
            status = self.table.table_status
            self.assertEqual(status, 'ACTIVE')
            print("✅ Connection Successful")
        except Exception as e:
            self.fail(f"Connection failed: {e}")

    def test_crud_operations(self):
        """Test Insert, Get, Update, Delete"""
        print("\nTesting CRUD operations...")
        item_id = "TEST_ITEM_999"
        
        # 1. Put Item
        self.table.put_item(Item={
            'id': item_id,
            'name': 'Test Project Scylla',
            'value': Decimal('10.5')
        })
        
        # 2. Get Item
        response = self.table.get_item(Key={'id': item_id})
        self.assertIn('Item', response)
        self.assertEqual(response['Item']['name'], 'Test Project Scylla')
        self.assertEqual(response['Item']['value'], Decimal('10.5'))
        print("✅ PUT/GET passed")

        # 3. Update Item
        self.table.update_item(
            Key={'id': item_id},
            UpdateExpression='SET #n = :val',
            ExpressionAttributeNames={'#n': 'name'},
            ExpressionAttributeValues={':val': 'Updated Name'}
        )
        response = self.table.get_item(Key={'id': item_id})
        self.assertEqual(response['Item']['name'], 'Updated Name')
        print("✅ UPDATE passed")

        # 4. Delete Item
        self.table.delete_item(Key={'id': item_id})
        response = self.table.get_item(Key={'id': item_id})
        self.assertNotIn('Item', response)
        print("✅ DELETE passed")

if __name__ == '__main__':
    unittest.main()
