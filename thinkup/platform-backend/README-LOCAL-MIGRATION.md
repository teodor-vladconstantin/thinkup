# Local Migration to ScyllaDB Alternator

This guide explains how to run the backend with a local ScyllaDB Alternator instance (DynamoDB compatible).

## Prerequisites

- Docker and Docker Compose
- Python 3.x

## Setup

1.  **Start ScyllaDB**
    Run the following command in the `platform-backend` directory to start the local database:
    ```bash
    docker-compose up -d
    ```

2.  **Configure Environment**
    Create or update your `.env` file in `platform-backend/` with the following variable:
    ```env
    DYNAMODB_ENDPOINT_URL=http://localhost:8000
    AWS_ACCESS_KEY_ID=local
    AWS_SECRET_ACCESS_KEY=local
    REGION_NAME=us-east-1
    ```
    (Detailed AWS usage might require dummy credentials as shown above if running purely local).

3.  **Initialize Database**
    Run the initialization script to create the required tables:
    ```bash
    python init_local_db.py
    ```

4.  **Run Backend**
    Run the backend normally:
    ```bash
    python src/main.py
    ```

## Reverting to AWS

To revert to using the real AWS DynamoDB:
1.  Remove or comment out `DYNAMODB_ENDPOINT_URL` in your `.env` file (or set it to empty).
2.  Ensure your AWS credentials are correct.
