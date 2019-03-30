import unittest

from read.FileInfo import FileInfo


class TestFileInfo(unittest.TestCase):
    def setUp(self):
        lines = ['import json\n', 'import requests\n', '\n', '\n', '# this is the lambda\n', 'def lambda_handler(event, context):\n',
                 '    return {\n', '        "statusCode": 200,\n', '        "body": json.dumps({\n', '            "message": "hello world",\n', '        }),\n', '    }\n']
        self.fileInfo = FileInfo('/some/location', '/some/location/dir_of_lambda', '/some/location/dir_of_lambda/file.py', 'def my_handler(event, context):', lines)

    def test_build_camel_case_name(self):
        result = self.fileInfo.build_camel_case_name('hello_world')

        self.assertEqual(result, 'HelloWorld')

    def test_build_handler(self):
        result = self.fileInfo.build_handler()

        self.assertEqual(result, 'file.my_handler')

    def test_build(self):
        result = self.fileInfo.build()

        self.assertEqual(result['name'], 'DirOfLambda')
        self.assertEqual(result['handler'], 'file.my_handler')
        self.assertEqual(result['uri'], 'dir_of_lambda/')
