import os

import boto3

s3_client = boto3.client('sns')

BUCKET_NAME = os.environ['BUCKET_NAME']


def some_handler(event, context):
    # do something with our bucket
    return "hello world"
