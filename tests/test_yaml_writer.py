import unittest

from write import yaml_writer


class TestPythonStrategy(unittest.TestCase):
    def test_create_role_adds_correct_permissions(self):
        result = yaml_writer.create_role(['dynamodb:*', 's3:*'])

        self.assertEqual(result['Type'], 'AWS::IAM::Role')
        self.assertEqual(result['Properties']['Policies'][0]['PolicyDocument']['Statement'][0]['Action'], ['logs:CreateLogStream', 'logs:CreateLogGroup', 'logs:PutLogEvents', 'dynamodb:*', 's3:*'])

    def test_create_role_name(self):
        result = yaml_writer.create_role_name('HelloWorldLambda')

        self.assertEqual(result, 'HelloWorldLambdaRole')

    def test_write_header(self):
        result = yaml_writer.write_header()

        self.assertEqual(result['AWSTemplateFormatVersion'], '2010-09-09')
        self.assertEqual(result['Transform'], 'AWS::Serverless-2016-10-31')

    def test_create_event_name(self):
        result = yaml_writer.create_event_name('HelloLambda', 'DynamoDB')

        self.assertEqual(result, 'HelloLambdaDynamoDBEvent')

    def test_create_lambda_function(self):
        result = yaml_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', ['BUCKET'], ['S3'])

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role'], '!GetAtt HelloLambdaRole.Arn')
        self.assertEqual(properties['Environment']['BUCKET'], 'Fill in value or delete if not needed')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Type'], 'S3')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Bucket'], 'Fill in value and change event - object created - if needed')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Events'], 's3:ObjectCreated:*')

    def test_create_lambda_function_no_events(self):
        result = yaml_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', ['BUCKET'], [])

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role'], '!GetAtt HelloLambdaRole.Arn')
        self.assertEqual(properties['Environment']['BUCKET'], 'Fill in value or delete if not needed')
        self.assertFalse('Events' in properties)

    def test_create_lambda_function_no_variables(self):
        result = yaml_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', [], ['S3'])

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role'], '!GetAtt HelloLambdaRole.Arn')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Type'], 'S3')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Bucket'], 'Fill in value and change event - object created - if needed')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Events'], 's3:ObjectCreated:*')
        self.assertFalse('Environment' in properties)

    def test_create_lambda_function_no_variables_or_events(self):
        result = yaml_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', [], [])

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role'], '!GetAtt HelloLambdaRole.Arn')
        self.assertFalse('Events' in properties)
        self.assertFalse('Environment' in properties)
