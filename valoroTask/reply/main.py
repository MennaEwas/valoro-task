import json
import logging
import db_connection
from valoro_orm_objects import Reply

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)

session = db_connection.get_db_session()

def get_replies():
    try:
        replies = session.query(Reply)
        results = [
            { "id": reply.id,
              "title": reply.replyTitle,
              "comment": reply.replyComment,
              "voice_not_link": reply.voiceNoteLink
            }
            for reply in replies
        ]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "replies": results
            })
        }
    except Exception as e:
        logger.debug(e)
        return {
            "statusCode": 500,
            "error": f"Error: {e}"
        }


def add_reply(event):
    try:
        req = json.loads(event['body'])
        if 'title' not in req:
           return {
            "statusCode": 400,
            "error": "Reply should has a title"
            }
        reply = Reply(replyTitle=req['title'], replyComment=req['comment'], voiceNoteLink=req['voice_note_file_name']) 
        logger.debug(f"Inserting: {reply}")
        session.add(reply)
        session.commit()

        return {
            "statusCode": 200
        }
    except Exception as e:
        logger.debug(e)
        return {
            "statusCode": 500,
            "error": f"Error: {e}"
        }

"""
def update_reply(event):
    try:
        req = json.loads(event['body'])
        reply = Reply.query.filter_by(replyTitle=req['title']).first()
        if 'title' in req:
            reply.replyTitle = req['title']
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

"""

def lambda_handler(event, context):
    
    logger.debug(event)
    print(event)

    if (event['httpMethod'] == 'POST'):
        response = add_reply(event)
    elif (event['httpMethod'] == 'GET'):
        response = get_replies()
    else:
        logger.debug(f"No handler for http verb: {event['httpMethod']}")
        raise Exception(f"No handler for http verb: {event['httpMethod']}")
        
    return response