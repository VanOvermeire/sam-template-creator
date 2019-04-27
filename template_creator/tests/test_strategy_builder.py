import unittest

from template_creator.reader import language_strategy_builder
from template_creator.reader.PythonStrategy import PythonStrategy
from template_creator.reader.GoStrategy import GoStrategy
from template_creator.util.template_errors import LanguageError


class TestStrategyBuilder(unittest.TestCase):
    def test_build_strategy_returns_correct_strategy_for_language_python(self):
        result = language_strategy_builder.build_strategy('python3.7')

        self.assertTrue(isinstance(result, PythonStrategy))

    def test_build_strategy_returns_correct_strategy_for_language_go(self):
        result = language_strategy_builder.build_strategy('go')

        self.assertTrue(isinstance(result, GoStrategy))

    def test_build_strategy_throws_exception_for_unknown_language(self):
        with self.assertRaises(LanguageError):
            language_strategy_builder.build_strategy('fake')

    def test_is_handler_line_with_handler_present_returns_true(self):
        lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                 '# this is the lambda\n', 'def lambda_handler(event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                 '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        is_handler_file, handler_line = language_strategy_builder.is_handler_file_for('python3.7', lines)

        self.assertTrue(is_handler_file)
        self.assertTrue('def lambda_handler(event, context):' in handler_line)

    def test_is_handler_line_with_handler_not_present_returns_false(self):
        lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                 '# this is the lambda\n', '    return {\n', '        "statusCode": 200,\n',
                 '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        is_handler_file, handler_line = language_strategy_builder.is_handler_file_for('python3.7', lines)

        self.assertFalse(is_handler_file)
