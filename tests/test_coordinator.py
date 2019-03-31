import unittest
from unittest.mock import patch

import coordinator


class TestCoordinator(unittest.TestCase):
    def test_full_location_template_without_ending_forward_slash(self):
        result = coordinator.full_location_template('/some/location', 'template.yaml')

        self.assertEqual(result, '/some/location/template.yaml')

    def test_full_location_template_with_ending_forward_slash(self):
        result = coordinator.full_location_template('/some/location/', 'template.yaml')

        self.assertEqual(result, '/some/location/template.yaml')

    @patch('write.yaml_writer.write')
    @patch('read.directory_scanner.find_directory')
    @patch('read.directory_scanner.guess_language')
    @patch('checks.checks.check_template_name')
    def test_create_template(self, checks_mock, guess_language_mock, find_dir_mock, yaml_mock):
        guess_language_mock.return_value = 'python3.7'
        guess_language_mock.find_directory('/some/location', 'python3.7').return_value = {}
        checks_mock.return_value = None
        find_dir_mock.return_value = {}
        yaml_mock.return_value = None

        coordinator.create_template('/some/location', None, None, None)

        yaml_mock.assert_called_once_with({'language': 'python3.7', 'lambdas': {}, 'location': '/some/location/template.yaml', 'memory': 512, 'timeout': 3})
