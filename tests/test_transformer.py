import unittest

from middleware import transformer


class TestTransformer(unittest.TestCase):
    def test(self):
        lambdas = [{'events': ['S3', 'SNS']}]

        result = transformer.add_to_resources(lambdas)

        self.assertEqual(list(result.keys()), ['S3EventBucket'])
        self.assertEqual(result['S3EventBucket']['Type'], 'AWS::S3::Bucket')