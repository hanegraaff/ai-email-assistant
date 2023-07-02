import json

def handler(event, context):
    
    try:
        path = event['requestContext']['resourcePath']
    except Exception as e:
        return get_response(500, "Could not read request path")
    
    
    return get_response(200, json.dumps(event))

    
def get_response(status_code : int, body : str): #-> dict
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': body,
        "isBase64Encoded": False
    }