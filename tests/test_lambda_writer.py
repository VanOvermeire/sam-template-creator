import unittest

from write import lambda_writer


class TestLambdaWriter(unittest.TestCase):
    def test_create_role_adds_correct_permissions(self):
        name, role = lambda_writer.create_role('HelloWorld', ['dynamodb:*', 's3:*'])

        self.assertEqual(name, 'HelloWorldRole')
        self.assertEqual(role['Type'], 'AWS::IAM::Role')
        self.assertEqual(role['Properties']['Policies'][0]['PolicyDocument']['Statement'][0]['Action'], ['logs:CreateLogStream', 'logs:CreateLogGroup', 'logs:PutLogEvents', 'dynamodb:*', 's3:*'])

    def test_create_role_name(self):
        result = lambda_writer.create_role_name('HelloWorldLambda')

        self.assertEqual(result, 'HelloWorldLambdaRole')

    def test_create_event_name(self):
        result = lambda_writer.create_event_name('HelloLambda', 'DynamoDB')

        self.assertEqual(result, 'HelloLambdaDynamoDBEvent')

    def test_create_lambda_function(self):
        result = lambda_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', ['BUCKET'], ['S3'])

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role']['Fn::GetAtt'], ['HelloLambdaRole', 'Arn'])
        self.assertEqual(properties['Environment']['Variables']['BUCKET'], 'Fill in value or delete if not needed')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Type'], 'S3')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Bucket']['Ref'], 'S3EventBucket')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Events'], 's3:ObjectCreated:*')

    def test_create_lambda_function_no_events(self):
        result = lambda_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', ['BUCKET'], [])

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role']['Fn::GetAtt'], ['HelloLambdaRole', 'Arn'])
        self.assertEqual(properties['Environment']['Variables']['BUCKET'], 'Fill in value or delete if not needed')
        self.assertFalse('Events' in properties)

    def test_create_lambda_function_no_variables(self):
        result = lambda_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', [], ['S3'])

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role']['Fn::GetAtt'], ['HelloLambdaRole', 'Arn'])
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Type'], 'S3')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Bucket']['Ref'], 'S3EventBucket')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Events'], 's3:ObjectCreated:*')
        self.assertFalse('Environment' in properties)

    def test_create_lambda_function_no_variables_or_events(self):
        result = lambda_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', [], [])

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role']['Fn::GetAtt'], ['HelloLambdaRole', 'Arn'])
        self.assertFalse('Events' in properties)
        self.assertFalse('Environment' in properties)
