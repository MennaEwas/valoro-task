import json
import os
import logging

import boto3
from valoro_orm_objects import Base
from valoro_utils import create_db_engine
from crhelper import CfnResource

logger = logging.getLogger(__name__)
cfn_helper = CfnResource(json_logging=False, log_level="DEBUG", boto_level="CRITICAL")
db_secret_name = os.getenv('DB_SECRET_NAME')
db_proxy_endpoint = os.getenv('DB_PROXY_ENDPOINT')
secrets_client = boto3.client('secretsmanager')

# Get DB credentials from AWS Secrets Manager
def get_db_secrets():
    """
    Return the secret string as a dictionary for secret name SECRET_NAME.
    """
    secret_response = secrets_client.get_secret_value(SecretId=db_secret_name)
    secrets = json.loads(secret_response['SecretString'])
    return secrets

@cfn_helper.create
@cfn_helper.update
def create(event, context):
    """
    DB Schema creation/update Lambda function entry point
    """
    global resource_id

    logger.info(f'Retrieving database access information from Secrets Manager\'s secret: "{db_secret_name}"')
    secrets = get_db_secrets()
    db_name = secrets['dbname']
    db_conn_string = f"postgresql://{secrets['username']}:{secrets['password']}@{db_proxy_endpoint}:{secrets['port']}/{db_name}?sslmode=require"

    logger.info(f'Creating SQLAlchemy database engine for database: "{db_name}"')
    engine = create_db_engine(db_conn_string)

    logger.info(f'Creating or Updating DB schema for database: "{db_name}"')
    Base.metadata.create_all(engine)

    return f'{db_name}-schema'

@cfn_helper.delete
def no_op(event, context):
    """
    Needed for the custom resource to delete properly.
    """
    logger.info('No action required when deleting this resource')

def lambda_handler(event, context):
    """
    Lambda entry point.
    """
    cfn_helper(event, context)
