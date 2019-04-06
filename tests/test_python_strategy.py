import unittest

from read.PythonStrategy import PythonStrategy


class TestPythonStrategy(unittest.TestCase):

    def setUp(self):
        self.lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                      '# this is the lambda\n', 'def lambda_handler(s3event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                      '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']
        self.hander_line = 'def my_handler(s3event, context):'
        self.strategy = PythonStrategy('../read/config/python_iam_exceptions')

    def test_find_env_variables(self):
        result = self.strategy.find_env_variables(self.lines)

        self.assertEqual(result, ['variable'])

    def test_find_role(self):
        result = self.strategy.find_role(self.lines)

        self.assertEqual(result, ['dynamodb:*'])

    def test_find_exceptional_role(self):
        self.lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('stepfunctions')\n", "var = os.environ['variable']\n", '\n', '\n',
                      '# this is the lambda\n', 'def lambda_handler(s3event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                      '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        result = self.strategy.find_role(self.lines)

        self.assertEqual(result, ['states:*'])

    def test_find_events(self):
        result = self.strategy.find_events(self.hander_line)

        self.assertEqual(result, ['S3'])

    def test_find_events_with_underscore_in_name_event(self):
        result = self.strategy.find_events('def my_handler(sqs_event, context):')

        self.assertEqual(result, ['SQS'])

    def test_build_handler(self):
        result = self.strategy.build_handler('/some/location/dir_of_lambda', '/some/location/dir_of_lambda/file.py', self.hander_line)

        self.assertEqual(result, 'file.my_handler')

    def test_find_api_no_api(self):
        result = self.strategy.find_api(self.hander_line)

        self.assertEqual(result, [])

    def test_find_api_second_no_api(self):
        result = self.strategy.find_api('def some_handler(s3event, context):')

        self.assertEqual(result, [])

    def test_find_api_simple_with_method_first(self):
        result = self.strategy.find_api('def put_add_handler(s3event, context):')

        self.assertEqual(result, ['put', '/add'])

    def test_find_api_simple_with_method_second(self):
        result = self.strategy.find_api('def add_put_handler(s3event, context):')

        self.assertEqual(result, ['put', '/add'])

    def test_find_api_multiple_levels_with_method_first(self):
        result = self.strategy.find_api('def put_add_hello_handler(s3event, context):')

        self.assertEqual(result, ['put', '/add/hello'])
