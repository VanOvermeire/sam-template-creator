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

    # TODO several tests for this one
    def test_create_lambda_function(self):
        pass
        # yaml_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', '')

    # def test_write_resources(self):
