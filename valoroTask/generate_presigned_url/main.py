import boto3
import json
import os
import logging
import uuid
from botocore.client import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
db_secret_name = os.getenv('DB_SECRET_NAME')
secrets_client = boto3.client('secretsmanager')

# Get DB credentials from AWS Secrets Manager
def get_db_secrets():
    """
    Return the secret string as a dictionary for secret name SECRET_NAME.
    """
    secret_response = secrets_client.get_secret_value(SecretId=db_secret_name)
    secrets = json.loads(secret_response['SecretString'])
    return secrets

def lambda_response(res, httpStatusCode):
    return {
        "isBase64Encoded": False,
        "statusCode": httpStatusCode,
        "headers": { "Content-Type": "*/*", " Access-Control-Allow-Origin:": "*"},
        "body": res
    }

def create_presigned_url(event):
    try:
        bucket_name = get_db_secrets()['bucketname']
        file_name = uuid.uuid4().hex
        s3_client = boto3.client("s3", config=Config(signature_version='s3v4'))
        url = s3_client.generate_presigned_url('put_object',Params={'Bucket': bucket_name,'Key': file_name},ExpiresIn=3600, HttpMethod='PUT')
        return lambda_response(json.dumps({"url": url, "file_name": file_name}), 200)
    except Exception as e:
        logger.debug(e)
        return lambda_response(json.dumps({"error": f"Error: {e}"}), 500)

def lambda_handler(event, context):
    
    logger.debug(event)
    if (event['httpMethod'] == 'GET'):
        response = create_presigned_url(event)
    else:
        logger.debug(f"No handler for http verb: {event['httpMethod']}")
        raise Exception(f"No handler for http verb: {event['httpMethod']}")
        
    return response