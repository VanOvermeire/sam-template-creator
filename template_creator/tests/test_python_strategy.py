import unittest

from template_creator.reader.PythonStrategy import PythonStrategy


class TestPythonStrategy(unittest.TestCase):

    def setUp(self):
        self.lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                      '# this is the lambda\n', 'def lambda_handler(s3event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                      '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']
        self.hander_line = 'def my_handler(s3event, context):'
        self.strategy = PythonStrategy()

    def test_is_handler_file(self):
        is_handler, line = self.strategy.is_handler_file(self.lines)

        self.assertTrue(is_handler)
        self.assertEqual(line, 'def lambda_handler(s3event, context):\n')

    def test_is_not_handler_file(self):
        lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                 '# this is the lambda\n', '    return {\n', '        "statusCode": 200,\n',
                 '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        is_handler, line = self.strategy.is_handler_file(lines)

        self.assertFalse(is_handler)

    def test_find_env_variables(self):
        result = self.strategy.find_env_variables(self.lines)

        self.assertEqual(result, ['variable'])

    def test_find_multiple_env_variables(self):
        self.lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n",
                      "callToFunction(os.environ['variable'],os.environ['second'])\n",
                      'def lambda_handler(s3event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                      '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        result = self.strategy.find_env_variables(self.lines)

        self.assertCountEqual(result, ['variable', 'second'])

    def test_find_env_variables_environ_get(self):
        self.lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n",
                      "callToFunction(os.environ.get('variable'))\n",
                      'def lambda_handler(s3event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                      '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        result = self.strategy.find_env_variables(self.lines)

        self.assertCountEqual(result, ['variable'])

    def test_find_role(self):
        result = self.strategy.find_permissions(self.lines)

        self.assertEqual(result, ['dynamodb:*'])

    def test_find_exceptional_role(self):
        self.lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('stepfunctions')\n", "var = os.environ['variable']\n", '\n', '\n',
                      '# this is the lambda\n', 'def lambda_handler(s3event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                      '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        result = self.strategy.find_permissions(self.lines)

        self.assertEqual(result, ['states:*'])

    def test_find_events(self):
        result = self.strategy.find_events(self.hander_line)

        self.assertEqual(result, ['S3'])

    def test_find_events_with_underscore_in_name_event(self):
        result = self.strategy.find_events('def my_handler(sqs_event, context):')

        self.assertEqual(result, ['SQS'])

    def test_find_events_no_events(self):
        result = self.strategy.find_events('def my_handler(an_event, context):')

        self.assertIsNone(result)

    def test_build_handler(self):
        result = self.strategy.build_handler('/some/location/dir_of_lambda', '/some/location/dir_of_lambda/file.py', self.hander_line, None)

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
        result = self.strategy.find_api('def add_post_handler(s3event, context):')

        self.assertEqual(result, ['post', '/add'])

    def test_find_api_multiple_levels_with_method_first(self):
        result = self.strategy.find_api('def put_add_hello_handler(s3event, context):')

        self.assertEqual(result, ['put', '/add/hello'])

    def test_find_invoked_files(self):
        handler_lines = ['import os\n', '\n', '# import commented.out\n', 'from util.util_functions import get_beautiful_page, publish_to_sns\n', 'import secondutil.moreutil\n',
                         'from thirdutil import evenmoreutil\n', '\n', "BASE_URL = os.environ['BASE_URL']\n", "sns_client = boto3.client('sns')\n", 'def handler(schedule_event, context):\n',
                         "    return {'result': 'done'}\n"]

        results = self.strategy.find_invoked_files(handler_lines)

        print(results)
        self.assertEqual(results['util'], 'util_functions')
        self.assertEqual(results['secondutil'], 'moreutil')
        self.assertEqual(results['thirdutil'], 'evenmoreutil')
