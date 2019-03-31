import unittest

from read import directory_scanner


class TestDirectoryScanner(unittest.TestCase):
    def test_is_handler_line_with_handler_present_returns_true(self):
        lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                 '# this is the lambda\n', 'def lambda_handler(event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                 '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        true, handler_line = directory_scanner.is_handler_file(lines)

        self.assertTrue(true)
        self.assertTrue('def lambda_handler(event, context):' in handler_line)

    def test_is_handler_line_with_handler_not_present_returns_false(self):
        lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                 '# this is the lambda\n', '    return {\n', '        "statusCode": 200,\n',
                 '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        true, handler_line = directory_scanner.is_handler_file(lines)

        self.assertFalse(true)

    def test_get_number_of_files_for_should_return_correct_number_of_files_for_suffix(self):
        result = directory_scanner.get_number_of_files_for('.py', ['some_file.py', 'secondfile.js', 'third_file.json', 'fourth.py'])

        self.assertEqual(result, 2)
