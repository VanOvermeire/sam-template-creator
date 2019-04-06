import unittest

from write import yaml_writer


class TestYamlWriter(unittest.TestCase):

    def test_write_header(self):
        result = yaml_writer.write_header()

        self.assertEqual(result['AWSTemplateFormatVersion'], '2010-09-09')
        self.assertEqual(result['Transform'], 'AWS::Serverless-2016-10-31')

    def test_write_globa(self):
        result = yaml_writer.write_global_section('python3.7', 512, 3)

        globals_function = result['Globals']['Function']

        self.assertEqual(globals_function['Timeout'], 3)
        self.assertEqual(globals_function['Runtime'], 'python3.7')
        self.assertEqual(globals_function['MemorySize'], 512)
