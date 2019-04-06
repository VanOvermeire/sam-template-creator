import boto3

client = boto3.client('s3')


def post_hello_world_handler(event, context):
    return ""
