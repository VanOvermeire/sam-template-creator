import unittest

from write import yaml_writer


# TODO add more tests
class TestPythonStrategy(unittest.TestCase):
    def test_create_role_adds_correct_permissions(self):
        result = yaml_writer.create_role(['dynamodb:*', 's3:*'])

        self.assertEqual(result['Type'], 'AWS::IAM::Role')
        self.assertEqual(result['Properties']['Policies'][0]['PolicyDocument']['Statement'][0]['Action'], ['logs:CreateLogStream', 'logs:CreateLogGroup', 'logs:PutLogEvents', 'dynamodb:*', 's3:*'])
