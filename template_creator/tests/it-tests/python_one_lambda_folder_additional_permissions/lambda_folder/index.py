import boto3

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')


def some_handler(event, context):
    return "hello world"
