
import boto3
import json
import base64
import hashlib

print('Loading function')
dynamo = boto3.resource('dynamodb').Table('NGStates')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': str(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def get_data(event):
    x = event['queryStringParameters']
    res = dynamo.get_item(Key=x)
    item = res.get("Item")
    if not item:
        return respond(KeyError('No key given'))
    return respond(None, item)


def post_data(event):
    payload = json.dumps(event.get('payload'))

    # hash the payload
    payload_hash = hashlib.sha1(payload.encode())

    # create a base64 version of the hash (& take the first 10 values)
    # Bytes object
    NGStateID_base64 = base64.urlsafe_b64encode(
        payload_hash.digest()[:10])
    # String
    NGStateID = NGStateID_base64.decode('utf-8').rstrip('=')

    # must include NGStateID
    data = {
        'NGStateID': NGStateID,
        'data': payload
    }
    res = dynamo.put_item(Item=data)

    if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
        msg = "Success"
    else:
        msg = "Failure"
    print(msg)
    print(json.dumps(res, indent=2))

    # return the ID
    return respond(None, NGStateID)


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    print("Received event: " + json.dumps(event, indent=2))

    operation = event['httpMethod']

    if operation == 'GET':
        get_data(event)
    elif operation == 'POST':
        post_data(event)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
