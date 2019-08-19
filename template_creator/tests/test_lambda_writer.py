import unittest

from template_creator.writer import lambda_writer


class TestLambdaWriter(unittest.TestCase):

    def test_find_existing_env_variables(self):
        first_resource = {'Type': 'AWS::Serverless::Function', 'Properties': {'Environment': {'Variables': {'BUCKET_NAME': 'my-own-bucket-name'}}}}
        second_resource = {'Type': 'AWS::Serverless::Function', 'Properties': {}}
        third_resource = {'Type': 'AWS::Role'}
        fourth_resource = {'Type': 'AWS::Serverless::Function', 'Properties': {'Environment': {'Variables': {'BUCKET_NAME': 'my-own-bucket-name'}}}}
        fifth_resource = {'Type': 'AWS::Serverless::Function', 'Properties': {'Environment': {'Variables': {'SNS_TOPIC': 'sns-topic-name'}}}}

        template_dict = {'Resources': {'First': first_resource, 'Second': second_resource, 'Third': third_resource, 'Fourth': fourth_resource, 'Fifth': fifth_resource}}

        result = lambda_writer.find_existing_env_var_values(template_dict)

        self.assertDictEqual(result, {'BUCKET_NAME': 'my-own-bucket-name', 'SNS_TOPIC': 'sns-topic-name'})

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
        result = lambda_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', ['BUCKET'], ['S3'], [], {})

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role']['Fn::GetAtt'], ['HelloLambdaRole', 'Arn'])
        self.assertEqual(properties['Environment']['Variables']['BUCKET'], 'Fill in value or delete if not needed')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Type'], 'S3')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Bucket']['Ref'], 'S3EventBucket')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Events'], 's3:ObjectCreated:*')

    def test_create_lambda_function_existing_value(self):
        first_resource = {'Type': 'AWS::Serverless::Function', 'Properties': {'Environment': {'Variables': {'BUCKET': 'my-own-bucket-name'}}}}
        existing_template_dict = {'Resources': {'First': first_resource}}

        result = lambda_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', ['BUCKET'], ['S3'], [], existing_template_dict)

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role']['Fn::GetAtt'], ['HelloLambdaRole', 'Arn'])
        self.assertEqual(properties['Environment']['Variables']['BUCKET'], 'my-own-bucket-name')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Type'], 'S3')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Bucket']['Ref'], 'S3EventBucket')
        self.assertEqual(properties['Events']['HelloLambdaS3Event']['Properties']['Events'], 's3:ObjectCreated:*')

    def test_create_lambda_function_with_rate_schedule_event(self):
        result = lambda_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', [], ['Schedule:2 hours'], [], {})

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role']['Fn::GetAtt'], ['HelloLambdaRole', 'Arn'])
        self.assertEqual(properties['Events']['HelloLambdaScheduleEvent']['Type'], 'Schedule')
        self.assertEqual(properties['Events']['HelloLambdaScheduleEvent']['Properties']['Schedule'], 'rate(2 hours)')

    def test_create_lambda_function_no_events(self):
        result = lambda_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', ['BUCKET'], [], [], {})

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role']['Fn::GetAtt'], ['HelloLambdaRole', 'Arn'])
        self.assertEqual(properties['Environment']['Variables']['BUCKET'], 'Fill in value or delete if not needed')
        self.assertFalse('Events' in properties)

    def test_create_lambda_function_no_variables(self):
        result = lambda_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', [], ['S3'], [], {})

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
        result = lambda_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', [], [], [], {})

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Role']['Fn::GetAtt'], ['HelloLambdaRole', 'Arn'])
        self.assertFalse('Events' in properties)
        self.assertFalse('Environment' in properties)

    def test_create_lambda_function_api(self):
        result = lambda_writer.create_lambda_function('HelloLambda', 'file.handler', 'uridir', [], [], ['get', '/hello/world'], {})

        self.assertEqual(result['Type'], 'AWS::Serverless::Function')

        properties = result['Properties']

        self.assertEqual(properties['CodeUri'], 'uridir')
        self.assertEqual(properties['Handler'], 'file.handler')
        self.assertEqual(properties['Events']['GET']['Type'], 'Api')
        self.assertEqual(properties['Events']['GET']['Properties']['Path'], '/hello/world')
        self.assertEqual(properties['Events']['GET']['Properties']['Method'], 'get')

