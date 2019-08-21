import unittest
from mock import patch

from template_creator.writer import yaml_writer


class YamlWriterTest(unittest.TestCase):

    @patch('template_creator.writer.lambda_writer.create_role')
    def test_write_roles(self, create_mock):
        create_mock.return_value = 'rolename', 'role'

        lambdas = [{'name': 'firstLambda', 'permissions': ['dynamodb:*']}]

        result = yaml_writer._write_roles(lambdas)

        self.assertEqual(result['rolename'], 'role')

    @patch('template_creator.writer.lambda_writer.create_lambda_function')
    def test_write_lambdas_globals_true(self, create_mock):
        create_mock.return_value = 'lambda'

        lambdas = [{'name': 'firstLambda', 'handler': 'a handler', 'uri': 'a uri', 'variables': [], 'events': [], 'api': []}]

        result = yaml_writer._write_lambdas(lambdas, True, 'python3.7', {})

        self.assertEqual(result['firstLambda'], 'lambda')

    @patch('template_creator.writer.lambda_writer.create_lambda_function')
    def test_write_lambdas_globals_false(self, create_mock):
        create_mock.return_value = {'Name': 'lambda', 'Properties': {'Runtime': '', 'Timeout': 0, 'MemorySize': 0}}

        lambdas = [{'name': 'firstLambda', 'handler': 'a handler', 'uri': 'a uri', 'variables': [], 'events': [], 'api': []}]

        result = yaml_writer._write_lambdas(lambdas, False, 'python3.7', {})

        print(result)

        self.assertEqual(result['firstLambda']['Name'], 'lambda')
        self.assertEqual(result['firstLambda']['Properties']['Runtime'], 'python3.7')
        self.assertEqual(result['firstLambda']['Properties']['Timeout'], 3)
        self.assertEqual(result['firstLambda']['Properties']['MemorySize'], 512)
