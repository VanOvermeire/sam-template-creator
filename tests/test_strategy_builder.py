import unittest

from reader import language_strategy_builder
from reader.PythonStrategy import PythonStrategy


class TestStrategyBuilder(unittest.TestCase):
    def test_build_strategy_returns_correct_strategy_for_language(self):
        result = language_strategy_builder.build_strategy('python3.7')

        self.assertTrue(isinstance(result, PythonStrategy))

    def test_build_strategy_throws_exception_for_unknown_language(self):
        with self.assertRaises(Exception):
            language_strategy_builder.build_strategy('fake')

    def test_is_handler_line_with_handler_present_returns_true(self):
        lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                 '# this is the lambda\n', 'def lambda_handler(event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                 '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        true, handler_line = language_strategy_builder.is_handler_file_for('python3.7', lines)

        self.assertTrue(true)
        self.assertTrue('def lambda_handler(event, context):' in handler_line)

    def test_is_handler_line_with_handler_not_present_returns_false(self):
        lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                 '# this is the lambda\n', '    return {\n', '        "statusCode": 200,\n',
                 '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        true, handler_line = language_strategy_builder.is_handler_file_for('python3.7', lines)

        self.assertFalse(true)
