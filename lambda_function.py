from crhelper import CfnResource

helper = CfnResource()

@helper.create
@helper.update
def sum_2_numbers(event, _):
    sum = int(event['ResourceProperties']['No1']) + int(event['ResourceProperties']['No2'])
    helper.Data['Sum'] = sum
@helper.delete
def no_op(_, __):
    pass

def handler(event, context):
    helper(event, context)

'''
{   "RequestType":"Create",
   "ServiceToken":"arn:aws:lambda:us-east-1:457175632986:function:crhelper-sum-resource",
   "ResponseURL":"https://cloudformation-custom-resource-response-useast1.s3.amazonaws.com/arn%3Aaws%3Acloudformation%3Aus-east-1%3A457175632986%3Astack/my-test-custom-resource-stack/89a58d50-94ae-11ea-be00-0eb40de15aba%7CSumResource%7Ceffbe842-4471-4a68-ac29-228b309558b3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20200513T001318Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=AKIA6L7Q4OWTTDPGOFMG%2F20200513%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=59d133ae37113e2b3bf3410bf359c731aad9f3a5cc4bdab927a9cf0fc6d6edb5",
   "StackId":"arn:aws:cloudformation:us-east-1:457175632986:stack/my-test-custom-resource-stack/89a58d50-94ae-11ea-be00-0eb40de15aba",
   "RequestId":"effbe842-4471-4a68-ac29-228b309558b3",
   "LogicalResourceId":"SumResource",
   "ResourceType":"Custom::Summer",
   "ResourceProperties":{
      "ServiceToken":"arn:aws:lambda:us-east-1:457175632986:function:crhelper-sum-resource",
      "No2":"2",
      "No1":"1"
}
}
'''

'''
{
    "Status": "SUCCESS",
    "PhysicalResourceId": "my-test-custom-resource-stack_SumResource_8QNR46DC",
    "StackId": "arn:aws:cloudformation:us-east-1:457175632986:stack/my-test-custom-resource-stack/89a58d50-94ae-11ea-be00-0eb40de15aba",
    "RequestId": "effbe842-4471-4a68-ac29-228b309558b3",
    "LogicalResourceId": "SumResource",
    "Reason": "",
    "Data": {
        "Sum": 3
    }
}
'''
