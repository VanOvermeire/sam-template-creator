import unittest

from template_creator.reader.FileInfo import FileInfo
from template_creator.reader.PythonStrategy import PythonStrategy


class TestFileInfo(unittest.TestCase):
    def setUp(self):
        lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                 '# this is the lambda\n', 'def lambda_handler(s3event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                 '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']

        strategy = PythonStrategy()
        self.fileInfo = FileInfo('/some/location', '/some/location/dir_of_lambda', '/some/location/dir_of_lambda/file.py', 'def my_handler(s3event, context):', lines, strategy, [])

    def test_build_camel_case_name(self):
        result = self.fileInfo.build_camel_case_name('hello_world')

        self.assertEqual(result, 'HelloWorld')

    def test_build(self):
        result = self.fileInfo.build()

        self.assertEqual(result['name'], 'DirOfLambda')
        self.assertEqual(result['handler'], 'file.my_handler')
        self.assertEqual(result['uri'], 'dir_of_lambda/')
        self.assertEqual(result['variables'], ['variable'])
        self.assertEqual(result['permissions'], ['dynamodb:*'])

    def test_build_uri_with_zip_executable(self):
        lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                 '# this is the lambda\n', 'def lambda_handler(s3event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                 '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']
        strategy = PythonStrategy()
        file_info = FileInfo('/some/location', '/some/location/dir_of_lambda', '/some/location/dir_of_lambda/file.py', 'def my_handler(s3event, context):', lines, strategy, [],
                             '/some/location/dir_of_lambda/dist/handler.zip')

        result = file_info.build()

        self.assertEqual(result['uri'], 'dir_of_lambda/dist/handler.zip')

    def test_build_uri_with_go_executable(self):
        lines = ['import json\n', 'import os\n', '\n', 'import requests\n', 'import boto3\n', '\n', "db = boto3.client('dynamodb')\n", "var = os.environ['variable']\n", '\n', '\n',
                 '# this is the lambda\n', 'def lambda_handler(s3event, context):\n', '    return {\n', '        "statusCode": 200,\n',
                 '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']
        strategy = PythonStrategy()
        file_info = FileInfo('/some/location', '/some/location/dir_of_lambda', '/some/location/dir_of_lambda/file.py', 'def my_handler(s3event, context):', lines, strategy, [],
                             '/some/location/dir_of_lambda/main')

        result = file_info.build()

        self.assertEqual(result['uri'], 'dir_of_lambda/main')
