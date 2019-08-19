import unittest

from mock import patch

from template_creator.util import template_checks


class TestInputChecks(unittest.TestCase):
    def test_build_backup_name(self):
        result = template_checks.build_backup_name('template.yaml')

        self.assertFalse('template.yaml' == result)
        self.assertTrue('template' in result)
        self.assertTrue('.yaml' in result)

    @patch('template_creator.util.template_checks.get_existing_template_as_dict')
    @patch('os.listdir')
    @patch('os.rename')
    def test_no_rename_when_template_not_in_dir(self, rename_mock, listdir_mock, existing_template_mock):
        listdir_mock.return_value = ['somefile.py']
        existing_template_mock.return_value = {}

        result = template_checks.check_template_name('/some/location', 'default_template.yaml')

        self.assertIsNone(result)
        rename_mock.assert_not_called()

    @patch('template_creator.util.template_checks.build_backup_name')
    @patch('template_creator.util.template_checks.get_existing_template_as_dict')
    @patch('os.listdir')
    @patch('os.rename')
    def test_rename_when_template_in_dir(self, rename_mock, listdir_mock, existing_template_mock, backup_mock):
        listdir_mock.return_value = ['somefile.py', 'default_template.yaml']
        backup_mock.return_value = 'backup.yaml'
        existing_template_mock.return_value = {}

        result = template_checks.check_template_name('/some/location', 'default_template.yaml')

        self.assertIsNotNone(result)

        rename_mock.assert_called_once_with('/some/location/default_template.yaml', '/some/location/backup.yaml')
