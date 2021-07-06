import boto3
import json
import os
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
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


def generate_presigned_url(event):
    try:
        bucket_name = get_db_secrets()['bucketname']
        region_name = boto3.session.Sesstion().region_name
        req = json.loads(event['body'])

        s3_client = boto3.client("s3", region_name=region_name)
        fields = s3_client.generate_presigned_url('put_object',Params={'Bucket': bucket_name,'Key': req['file_name'],'ACL': 'public-read'},ExpiresIn=3600)
        return {
                "statusCode": 200,
                "body": json.dumps({
                        "fields": fields
                })
                }
    except Exception as e:
        logger.debug(e)
        return {
            "statusCode": 500,
            "error": f"Error: {e}"
        }

def lambda_handler(event, context):
    
    logger.debug(event)
    if (event['httpMethod'] == 'GET'):
        response = generate_presigned_url(event)
    else:
        logger.debug(f"No handler for http verb: {event['httpMethod']}")
        raise Exception(f"No handler for http verb: {event['httpMethod']}")
        
    return response