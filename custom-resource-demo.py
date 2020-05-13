import json
import time
from botocore.vendored import requests

def lambda_handler(event, context):
    print 'REQUEST BODY:n' + str(event)
    count = 1
    #count = int(event['ResourceProperties']['count'])    #Uncomment this line if you are configuring the number of retries through the CFN template
    attempts = 0
    if count <= 3:
        count = 3
    while attempts < count:
        try:
            if event['RequestType'] == 'Delete':
                print "delete"
                #The rest of your delete logic goes here
            elif event['RequestType'] == 'Create':
                print "create"
                #The rest of your create logic goes here
            elif event['RequestType'] == 'Update':
                print "update"
                #The rest of your update logic goes here
            responseStatus = 'SUCCESS'
            responseData = {'Success': 'Everything worked.'}
            break
        except:
            responseStatus = 'FAILURE'
            responseData = {'Failure': 'Something bad happened.'}
            attempts += 1
            time.sleep(3)
    sendResponse(event, context, responseStatus, responseData)
    
def sendResponse(event, context, responseStatus, responseData, reason=None, physical_resource_id=None):
    responseBody = {'Status': responseStatus,
                    'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
                    'PhysicalResourceId': physical_resource_id or context.log_stream_name,
                    'StackId': event['StackId'],
                    'RequestId': event['RequestId'],
                    'LogicalResourceId': event['LogicalResourceId'],
                    'Data': responseData}
    print 'RESPONSE BODY:n' + json.dumps(responseBody)
    responseUrl = event['ResponseURL']
    json_responseBody = json.dumps(responseBody)
    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }
    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print "Status code: " + response.reason
    except Exception as e:
        print "send(..) failed executing requests.put(..): " + str(e)