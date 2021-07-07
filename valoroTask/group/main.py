import json
import logging
from os import name
import db_connection
from valoro_orm_objects import Group
from jsonschema import validate

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

session = db_connection.get_db_session()
def lambda_response(res, httpStatusCode):
    return {
        "isBase64Encoded": False,
        "statusCode": httpStatusCode,
        "headers": { "Content-Type": "*/*", " Access-Control-Allow-Origin:": "*"},
        "body": res
    }

def get_groups():
    try:
        groups = session.query(Group)
        results = [
            group.format()
            for group in groups
        ]
        return lambda_response(json.dumps({"groups": results}), 200)
    except Exception as e:
        return lambda_response(json.dumps({"error": f"Error: {e}"}), 500)



def add_group(event):
    try:
        req = json.loads(event['body'])
        validate(instance=req, schema=Group.validationSchema())
        group = Group()
        if 'name' in req:
            group.name = req['name']
        if 'description' in req:
            group.group_description = req['description']
        if 'img' in req:
            group.img = req['img']
        if 'capacity' in req:
            group.capacity = req['capacity']
        if 'cost' in req:
            group.cost = req['cost']
        if 'group_type_id' in req:
            group.group_type_id = req['group_type_id'] 
        
        logger.debug(f"Inserting: {group}")
        session.add(group)
        session.commit()

        return lambda_response(json.dumps(group.format()), 200)
    except Exception as e:
        logger.debug(e)
        return lambda_response(json.dumps({"error": f"Error: {e}"}), 500)


def update_group(event):
    try:
        req = json.loads(event['body'])
        group = session.query(Group).filter_by(id=req['id']).first()
        if group is None:
            return lambda_response(json.dumps({"error": "Not Found"}), 404)
        
        validate(instance=req, schema=Group.validationSchema())
       
        if 'name' in req:
            group.name = req['name']
        if 'description' in req:
            group.group_description = req['description']
        if 'img' in req:
            group.img = req['img']
        if 'capacity' in req:
            group.capacity = req['capacity']
        if 'cost' in req:
            group.cost = req['cost']
        if 'group_type_id' in req:
            group.group_type_id = req['group_type_id'] 
        
        logger.debug(f"Updating: {group}")
        session.commit()

        return lambda_response(json.dumps(group.format()), 200)
    except Exception as e:
        logger.debug(e)
        return lambda_response(json.dumps({"error": f"Error: {e}"}), 500)



def lambda_handler(event, context):
    
    logger.debug(event)

    if (event['httpMethod'] == 'POST'):
        response = add_group(event)
    elif (event['httpMethod'] == 'GET'):
        response = get_groups()
    elif (event['httpMethod'] == 'PUT'):
        response = update_group(event)
    else:
        logger.debug(f"No handler for http verb: {event['httpMethod']}")
        raise Exception(f"No handler for http verb: {event['httpMethod']}")
        
    return response