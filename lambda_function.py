import base64
import gzip
import hashlib
import json

import boto3
from boto3.dynamodb import types

print("Loading function")
dynamo = boto3.resource("dynamodb").Table("NGStates")

URL = "https://json.neurodata.io/v1"


def response(message, status_code):
    # print('Message:', message)
    # print('Status code:', status_code)
    return {
        "statusCode": status_code,
        "body": message,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "isBase64Encoded": False,
    }


def get_data(event):
    x = event["queryStringParameters"]
    res = dynamo.get_item(Key=x)
    item = res.get("Item")
    if not item:
        msg = "Item not found in DynamoDB"
        # print(msg)
        return response(msg, 400)
    data = item.get("data")

    # backwards compatibility (data stored directly as JSON string)
    if type(data) == str:
        return response(json.loads(data), 200)
    # all data going forward is gzip compressed in dynamo to get around 400K limit
    elif type(data) == types.Binary:
        return response(json.loads(gzip.decompress(data.value)), 200)
    else:
        return response("type unsupported", 502)


def post_data(event):
    # payload as string
    payload = json.dumps(event.get("body"))

    # hash the payload
    payload_hash = hashlib.sha1(payload.encode())

    # create a base64 version of the hash (& take the first 10 values)
    # Bytes object
    NGStateID_base64 = base64.urlsafe_b64encode(payload_hash.digest()[:10])
    # String
    NGStateID = NGStateID_base64.decode("utf-8").rstrip("=")

    # must include NGStateID
    data = {"NGStateID": NGStateID, "data": gzip.compress(bytes(payload, "utf-8"))}
    res = dynamo.put_item(Item=data)

    if res["ResponseMetadata"]["HTTPStatusCode"] != 200:
        msg = "Post failure - database returned error code {}".format(
            res["ResponseMetadata"]["HTTPStatusCode"]
        )
        # print(msg)
        return response(msg, 500)

    # return the ID
    if event["path"] == "/v1":
        return response(
            json.dumps({"uri": "{}?NGStateID={}".format(URL, NGStateID)}), 201
        )
    else:
        return response(json.dumps("{}?NGStateID={}".format(URL, NGStateID)), 201)


def lambda_handler(event, context):
    """Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    """
    # print("Received event: " + json.dumps(event, indent=2))

    operation = event["httpMethod"]

    if operation == "GET":
        return get_data(event)
    elif operation == "POST":
        return post_data(event)
    else:
        return response('Unsupported method "{}"'.format(operation), 400)
