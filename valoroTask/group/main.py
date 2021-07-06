import json
import logging
from os import name
import db_connection
from valoro_orm_objects import Group

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

session = db_connection.get_db_session()

def get_groups():
    try:
        groups = session.query(Group)
        results = [
            { "id": group.id,
              "name": group.name,
              "img": group.img,
              "cost": group.cost,
              "description": group.description,
              "capacity": group.capacity
            }
            for group in groups
        ]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "groups": results
            })
        }
    except Exception as e:
        logger.debug(e)
        return {
            "statusCode": 500,
            "error": f"Error: {e}"
        }


def add_group(event):
    try:
        req = json.loads(event['body'])
        group = Group(
            name=req['name'],
            img=req['img'],
            description=req['description'],
            capacity=int(req['capacity']),
            cost = float(req['cost']),
            groupTypeId = int(req['group_type_id'])
        )
        logger.debug(f"Inserting: {group}")
        session.add(group)
        session.commit()

        return {
            "statusCode": 200
        }
    except Exception as e:
        logger.debug(e)
        print(e)
        return {
            "statusCode": 500,
            "error": f"Error: {e}"
        }

def update_group(event):
    try:
        req = json.loads(event['body'])
        group = Group.query.filter_by(name=req['name']).first()
        if 'name' in req:
            group.name = req['name']
        if 'description' in req:
            group.description = req['description']
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
    
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "group": group
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