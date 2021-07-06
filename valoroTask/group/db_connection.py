from valoro_utils import create_db_engine, create_db_session
import boto3
import json
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
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

# Get SQLAlchemy Session
def get_db_session():
    logger.info(f'Retrieving database access information from Secrets Manager\'s secret: "{db_secret_name}"')
    secrets = get_db_secrets()
    db_name = secrets['dbname']
    db_conn_string = f"postgresql://{secrets['username']}:{secrets['password']}@{db_proxy_endpoint}:{secrets['port']}/{db_name}?sslmode=require"
    
    logger.info(f'Creating SQLAlchemy database engine for database: "{db_name}"')
    engine = create_db_engine(db_conn_string)
    session = create_db_session(engine)
    return session