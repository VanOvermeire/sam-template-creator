import unittest

from write import yaml_writer


class TestYamlWriter(unittest.TestCase):

    def test_write_header(self):
        result = yaml_writer.write_header()

        self.assertEqual(result['AWSTemplateFormatVersion'], '2010-09-09')
        self.assertEqual(result['Transform'], 'AWS::Serverless-2016-10-31')

    def test_write_globa(self):
        result = yaml_writer.write_global_section('python3.7', 512, 3)
        # TODO test for global
