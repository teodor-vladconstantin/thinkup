import os

import boto3
from dotenv import load_dotenv

from dynamoDB.db_crud_goals import DB_CRUD_GOALS
from dynamoDB.db_crud_material import DB_CRUD_MATERIAL
from dynamoDB.db_crud_mentor_feedback import DB_CRUD_MENTOR_FEEDBACK
from dynamoDB.db_crud_personal_objectives import DB_CRUD_PERSONAL_OBJECTIVES
from dynamoDB.db_crud_project_tokens import DB_CRUD_PROJECT_TOKENS
from dynamoDB.db_crud_mentor_tokens import DB_CRUD_MENTOR_TOKENS
from dynamoDB.db_crud_projects import DB_CRUD_PROJECTS
from dynamoDB.db_crud_reviews import DB_CRUD_REVIEWS
from dynamoDB.db_crud_s3IDs import DB_CRUD_S3IDS
from dynamoDB.db_crud_s3IDsOpenSchool import DB_CRUD_S3IDS_OPENSCHOOL
from dynamoDB.db_crud_users import DB_CRUD_USERS

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('REGION_NAME')
DYNAMODB_ENDPOINT_URL = os.getenv('DYNAMODB_ENDPOINT_URL')

def startSetup(whichTable: str):
    """Start the setup of the dynamoDB

    Args:
        whichTable (str): table from dynamoDB

    Returns:
        _type_: _description_
    """
    resource = boto3.resource(
        'dynamodb',
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        region_name = REGION_NAME,
        endpoint_url=DYNAMODB_ENDPOINT_URL
    )
    table = resource.Table(whichTable)

    if(whichTable == "Users"):
        return DB_CRUD_USERS(table)
    elif(whichTable == "Goals"):
        return DB_CRUD_GOALS(table)
    elif whichTable == "S3-IDs":
        return DB_CRUD_S3IDS(table)
    elif whichTable == "Materials":
        return DB_CRUD_MATERIAL(table)
    elif whichTable == "S3-IDs-OpenSchool":
        return DB_CRUD_S3IDS_OPENSCHOOL(table)
    elif whichTable == "Personal-Objectives":
        return DB_CRUD_PERSONAL_OBJECTIVES(table)
    elif whichTable == "Project-Tokens":
        return DB_CRUD_PROJECT_TOKENS(table)
    elif whichTable == "Mentor-Tokens":
        return DB_CRUD_MENTOR_TOKENS(table)
    elif whichTable == "Reviews":
        return DB_CRUD_REVIEWS(table)
    elif whichTable == "Mentor-Feedback":
        return DB_CRUD_MENTOR_FEEDBACK(table)
    return DB_CRUD_PROJECTS(table)

   








