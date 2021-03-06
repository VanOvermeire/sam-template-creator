import unittest
from unittest.mock import patch

from template_creator import coordinator


class TestCoordinator(unittest.TestCase):
    def test_full_location_template_without_ending_forward_slash(self):
        result = coordinator.find_full_path_for_yaml_template('/some/location', 'template.yaml')

        self.assertEqual(result, '/some/location/template.yaml')

    def test_full_location_template_with_ending_forward_slash(self):
        result = coordinator.find_full_path_for_yaml_template('/some/location/', 'template.yaml')

        self.assertEqual(result, '/some/location/template.yaml')

    def test_set_default_if_needed_for_not_needed_returns_language(self):
        result = coordinator.set_default_if_needed_for('python3.7', '/some/location')

        self.assertEqual(result, 'python3.7')

    @patch('template_creator.reader.directory_scanner.guess_language')
    def test_set_default_if_needed_returns_probable_language(self, guess_language_mock):
        guess_language_mock.return_value = 'python3.7'
        result = coordinator.set_default_if_needed_for(None, '/some/location')

        self.assertEqual(result, 'python3.7')

    @patch('template_creator.middleware.transformer')
    @patch('template_creator.writer.yaml_writer.write')
    @patch('template_creator.reader.directory_scanner.find_lambda_files_in_directory')
    @patch('template_creator.reader.directory_scanner.guess_language')
    @patch('template_creator.util.template_checks.check_template_name')
    def test_create_template(self, checks_mock, guess_language_mock, find_dir_mock, yaml_mock, transformer_mock):
        guess_language_mock.return_value = 'python3.7'
        guess_language_mock.find_directory('/some/location', 'python3.7').return_value = {}
        checks_mock.return_value = {'AWSTemplateFormatVersion': '2010-09-09', 'Resources': {}}
        find_dir_mock.return_value = [{
            'name': 'lambda-name',
            'handler': 'a handler',
            'uri': 'a uri',
            'variables': [],
            'events': [],
            'permissions': [],
            'api': []
        }]
        yaml_mock.return_value = None
        transformer_mock.return_value = {}

        coordinator.find_resources_and_create_yaml_template('/some/location', None, False)

        yaml_mock.assert_called_once_with({'language': 'python3.7',
                                           'lambdas': [{
                                               'name': 'lambda-name',
                                               'handler': 'a handler',
                                               'uri': 'a uri',
                                               'variables': [],
                                               'events': [],
                                               'permissions': [],
                                               'api': []
                                           }],
                                           'other_resources': {},
                                           'location': '/some/location/template.yaml',
                                           'set-global': False,
                                           'existing_template': {'AWSTemplateFormatVersion': '2010-09-09', 'Resources': {}},
                                           })

    @patch('template_creator.middleware.transformer')
    @patch('template_creator.writer.yaml_writer.write')
    @patch('template_creator.reader.directory_scanner.find_lambda_files_in_directory')
    @patch('template_creator.reader.directory_scanner.guess_language')
    @patch('template_creator.util.template_checks.check_template_name')
    def test_create_template_no_lambdas(self, checks_mock, guess_language_mock, find_dir_mock, yaml_mock, transformer_mock):
        guess_language_mock.return_value = 'python3.7'
        guess_language_mock.find_directory('/some/location', 'python3.7').return_value = {}
        checks_mock.return_value = None
        find_dir_mock.return_value = []

        coordinator.find_resources_and_create_yaml_template('/some/location', None, False)

        yaml_mock.assert_not_called()
