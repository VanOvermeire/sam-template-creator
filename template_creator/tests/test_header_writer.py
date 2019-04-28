import unittest

from template_creator.writer import header_writer


class TestHeaderWriter(unittest.TestCase):

    def test_write_header(self):
        result = header_writer.write_header()

        self.assertEqual(result['AWSTemplateFormatVersion'], '2010-09-09')
        self.assertEqual(result['Transform'], 'AWS::Serverless-2016-10-31')

    def test_write_global(self):
        result = header_writer.write_global_section('python3.7', 512, 3)

        globals_function = result['Globals']['Function']

        self.assertEqual(globals_function['Timeout'], 3)
        self.assertEqual(globals_function['Runtime'], 'python3.7')
        self.assertEqual(globals_function['MemorySize'], 512)

    def test_write_headers_no_globals_false(self):
        config = {
            'language': 'python3.7',
            'memory': 128,
            'timeout': 5,
            'no-globals': False,
        }

        result = header_writer.write_headers(config)

        self.assertEqual(result['AWSTemplateFormatVersion'], '2010-09-09')
        self.assertEqual(result['Transform'], 'AWS::Serverless-2016-10-31')

        globals_function = result['Globals']['Function']

        self.assertEqual(globals_function['Timeout'], 5)
        self.assertEqual(globals_function['Runtime'], 'python3.7')
        self.assertEqual(globals_function['MemorySize'], 128)

    def test_write_headers_no_globals_true(self):
        config = {
            'language': 'python3.7',
            'memory': 128,
            'timeout': 5,
            'no-globals': True,
        }

        result = header_writer.write_headers(config)

        self.assertEqual(result['AWSTemplateFormatVersion'], '2010-09-09')
        self.assertEqual(result['Transform'], 'AWS::Serverless-2016-10-31')
        self.assertFalse('Globals' in result)
