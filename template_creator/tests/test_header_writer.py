import unittest

from template_creator.writer import header_writer


class TestHeaderWriter(unittest.TestCase):

    def test_write_header(self):
        result = header_writer.write_header()

        self.assertEqual(result['AWSTemplateFormatVersion'], '2010-09-09')
        self.assertEqual(result['Transform'], 'AWS::Serverless-2016-10-31')

    def test_write_global(self):
        result = header_writer.write_global_section('python3.7')

        globals_function = result['Globals']['Function']

        self.assertEqual(globals_function['Timeout'], 3)
        self.assertEqual(globals_function['Runtime'], 'python3.7')
        self.assertEqual(globals_function['MemorySize'], 512)

    def test_write_headers_set_global_true(self):
        config = {
            'language': 'python3.7',
            'set-global': True,
        }

        result = header_writer.write_headers(config)

        self.assertEqual(result['AWSTemplateFormatVersion'], '2010-09-09')
        self.assertEqual(result['Transform'], 'AWS::Serverless-2016-10-31')

        globals_function = result['Globals']['Function']

        self.assertEqual(globals_function['Timeout'], 3)
        self.assertEqual(globals_function['Runtime'], 'python3.7')
        self.assertEqual(globals_function['MemorySize'], 512)

    def test_write_headers_set_global_false(self):
        config = {
            'language': 'python3.7',
            'set-global': False,
        }

        result = header_writer.write_headers(config)

        self.assertEqual(result['AWSTemplateFormatVersion'], '2010-09-09')
        self.assertEqual(result['Transform'], 'AWS::Serverless-2016-10-31')
        self.assertFalse('Globals' in result)
