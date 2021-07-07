import json
import logging
import db_connection
from valoro_orm_objects import Reply
from jsonschema import validate

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)

session = db_connection.get_db_session()
def lambda_response(res, httpStatusCode):
    return {
        "isBase64Encoded": False,
        "statusCode": httpStatusCode,
        "headers": { "Content-Type": "*/*", " Access-Control-Allow-Origin:": "*"},
        "body": res
    }

def get_replies():
    try:
        replies = session.query(Reply)
        results = [
            reply.format()
            for reply in replies
        ]
        return lambda_response(json.dumps({"replies": results}), 200)
    except Exception as e:
        logger.debug(e)
        return lambda_response(json.dumps({"error": f"Error: {e}"}), 500)



def add_reply(event):
    try:
        req = json.loads(event['body'])
        validate(instance=req, schema=Reply.validationSchema())
        reply = Reply(req['title'])
        if 'comment' in req:
            reply.replyComment=req['comment']
        if 'voice_note_file_name' in req:
            reply.voiceNoteLink=req['voice_note_file_name']

        logger.debug(f"Inserting: {reply}")
        session.add(reply)
        session.commit()

        return lambda_response(json.dumps(reply.format()), 200)
    except Exception as e:
        logger.debug(e)
        return lambda_response(json.dumps({"error": f"Error: {e}"}), 500)



def update_reply(event):
    try:
        req = json.loads(event['body'])
        reply = session.query(Reply).filter_by(id=req['id']).first()
        
        if reply is None:
            return lambda_response(json.dumps({"error": "Not Found"}), 404)        
        
        if 'title' in req:
            reply.title = req['title']
        if 'comment' in req:
            reply.replyComment=req['comment']
        if 'voice_note_file_name' in req:
            reply.voiceNoteLink=req['voice_note_file_name']
        
        logger.debug(f"Updating: {reply}")
        session.commit()
    
        return lambda_response(json.dumps(reply.format()), 200)
    except Exception as e:
        logger.debug(e)
        return lambda_response(json.dumps({"error": f"Error: {e}"}), 500)


def lambda_handler(event, context):
    
    logger.debug(event)
    print(event)

    if (event['httpMethod'] == 'POST'):
        response = add_reply(event)
    elif (event['httpMethod'] == 'GET'):
        response = get_replies()
    elif (event['httpMethod'] == 'PUT'):
        response = update_reply()
    else:
        logger.debug(f"No handler for http verb: {event['httpMethod']}")
        raise Exception(f"No handler for http verb: {event['httpMethod']}")
        
    return response