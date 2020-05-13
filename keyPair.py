import boto3
import json
import time
import random
    
from botocore.vendored import requests
from botocore.exceptions import ClientError
    
    
# Defining Globals

'''
Recieved Payload 
{
    "StackId": "arn:aws:cloudformation:us-east-2:457175632986:stack/create-cx-resource/c8e37cc0-16cd-11ea-96b8-02848c93abf4",
    "ResponseURL": "https://cloudformation-custom-resource-response-useast2.s3.us-east-2.amazonaws.com/arn%3Aaws%3Acloudformation%3Aus-east-2%3A457175632986%3Astack/create-cx-resource/c8e37cc0-16cd-11ea-96b8-02848c93abf4%7CKeyPair%7C5182c01f-47c0-4e7a-b319-f82224609827?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20191204T193930Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=AKIAVRFIPK6PMQZL3WHJ%2F20191204%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Signature=8d81eb6d9327e31984e651326384d4e03d608667c7036c9695ca6c1e78c3ea71",
    "ResourceProperties": {
        "KeyPair": "cx-key-pair",
        "ServiceToken": "arn:aws:lambda:us-east-2:457175632986:function:test-cx-resource-Function-SQE6GGB5F48I"
    },
    "RequestType": "Create",
    "ServiceToken": "arn:aws:lambda:us-east-2:457175632986:function:test-cx-resource-Function-SQE6GGB5F48I",
    "ResourceType": "Custom::KeyPair",
    "RequestId": "5182c01f-47c0-4e7a-b319-f82224609827",
    "LogicalResourceId": "KeyPair"
}
'''
    
client = boto3.client('ec2')
    
def lambda_handler(event, context):
    
    print("Recieved Payload {}".format(json.dumps(event)))
    
    key_pair = event['ResourceProperties']['KeyPair']
    
    try: 
        if event['RequestType'] == 'Delete':
    
            print("Recieved a Delete Request...")
            print("Deleting the key-pair {}".format(key_pair))
    
            response = delete_key_pair(key_pair)
            sendResponse(event, context, key_pair, "SUCCESS", {} )
    
    
        elif event['RequestType'] == 'Update':
    
            print("Recieved a Update Event...")
            print("Update requests are not supported for this resource...")
            
            sendResponse(event, context, key_pair, "SUCCESS", {} )
    
        
        elif event['RequestType'] == 'Create':
    
            print("Recieved a Create Event...")
            print ("Creating the key-pair {}".format(key_pair))
    
            response = create_key_pair(key_pair)
            sendResponse(event, context, key_pair, "SUCCESS", response )
    
    except ClientError as e:
    
        if e.response['Error']['Code'] == 'ThrottlingException':
            count = 3
            attempts = 0
            while attempts < count:
                print("Retrying Function Execution...")
                time.sleep(random.expovariate(1))
                lambda_handler(event, context)
                attempts += 1
        elif e.response['Error']['Code'] == "InvalidKeyPair.NotFound":
            print("Key Pair Already Deleted, Sending Success...")
            sendResponse(event, context, key_pair, "SUCCESS", {} )
        else: 
            sendResponse(event, context, key_pair, "FAILED", {} )
    
    
    
def create_key_pair(key_pair):
    response = client.create_key_pair(KeyName=key_pair)
    return  response
    
def delete_key_pair(key_pair):
    response = client.delete_key_pair(KeyName=key_pair)
    return  response
    
def sendResponse(event, context, physicalid, responseStatus, responseData):
    responseBody = {'Status': responseStatus,
                    'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
                    'PhysicalResourceId': physicalid,
                    'StackId': event['StackId'],
                    'RequestId': event['RequestId'],
                    'LogicalResourceId': event['LogicalResourceId'],
                    'NoEcho': "true",
                    'Data': responseData}
    print("RESPONSE BODY {}".format(json.dumps(responseBody)))
    responseUrl = event['ResponseURL']
    json_responseBody = json.dumps(responseBody)
    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }
    response = requests.put(responseUrl,data=json_responseBody,headers=headers)
