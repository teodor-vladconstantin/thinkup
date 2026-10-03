"""Dump / restore every Scylla (Alternator) table as typed DynamoDB JSON.

Typed JSON ({"N": "3.5"}, {"SS": [...]}) keeps numbers exact and sets as sets,
so a restore gives back exactly what was dumped.

  python scripts/backup_db.py dump > backup.json
  python scripts/backup_db.py restore [--suffix -restored] < backup.json

--suffix restores into copies (e.g. Users-restored, created if missing)
instead of overwriting the live tables - use it to inspect a backup first.
"""
import json
import os
import sys

import boto3

client = boto3.client(
    'dynamodb',
    endpoint_url=os.environ.get('DYNAMODB_ENDPOINT_URL', 'http://127.0.0.1:8000'),
    region_name=os.environ.get('AWS_REGION', 'eu-central-1'),
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', 'local'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', 'local'),
)


def dump():
    backup = {}
    for name in client.list_tables()['TableNames']:
        desc = client.describe_table(TableName=name)['Table']
        items = []
        for page in client.get_paginator('scan').paginate(TableName=name):
            items.extend(page['Items'])
        backup[name] = {
            'KeySchema': desc['KeySchema'],
            'AttributeDefinitions': desc['AttributeDefinitions'],
            'Items': items,
        }
        print(f"{name}: {len(items)}", file=sys.stderr)
    json.dump(backup, sys.stdout)


def restore(suffix=''):
    backup = json.load(sys.stdin)
    existing = set(client.list_tables()['TableNames'])
    for name, table in backup.items():
        target = name + suffix
        if target not in existing:
            client.create_table(TableName=target, KeySchema=table['KeySchema'],
                                AttributeDefinitions=table['AttributeDefinitions'],
                                BillingMode='PAY_PER_REQUEST')
        items = table['Items']
        for i in range(0, len(items), 25):  # batch_write_item takes at most 25
            requests = {target: [{'PutRequest': {'Item': it}} for it in items[i:i + 25]]}
            while requests:
                requests = client.batch_write_item(RequestItems=requests).get('UnprocessedItems')
        print(f"{target}: {len(items)}", file=sys.stderr)


if __name__ == '__main__':
    if sys.argv[1:2] == ['dump']:
        dump()
    elif sys.argv[1:2] == ['restore']:
        restore(sys.argv[3] if sys.argv[2:3] == ['--suffix'] else '')
    else:
        sys.exit(__doc__)
