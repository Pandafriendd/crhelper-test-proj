zip -r ../sum.zip ./
aws lambda create-function \
    --function-name "crhelper-sum-resource" \
    --handler "lambda_function.handler" \
    --timeout 900 \
    --zip-file fileb://../sum.zip \
    --runtime python3.7 \
    --role "arn:aws:iam::457175632986:role/lambda-cli-role"