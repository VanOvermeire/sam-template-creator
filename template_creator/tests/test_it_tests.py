import collections
import os
import unittest

from ruamel import yaml

from template_creator import coordinator

Location = collections.namedtuple('Locations', 'project expected result')


# TODO some more tests, including a few for Go
class ITTests(unittest.TestCase):

    def setUp(self) -> None:
        self.tests_location = 'it-tests'
        self.templates = 'templates'

    def test_one_lambda_basic_permissions(self):
        # TODO codeuri is generated as ./ Which should work, but could be cleaner without the /
        location = self.build_locations('one_lambda_basic_permissions')

        coordinator.find_resources_and_create_yaml_template(location.project, None, False)

        self.assert_result_equal_to_expected(location)

        self.cleanup(location)

    def test_one_lambda_in_folder_additional_permissions(self):
        location = self.build_locations('one_lambda_folder_additional_permissions')

        coordinator.find_resources_and_create_yaml_template(location.project, None, False)

        self.assert_result_equal_to_expected(location)

        self.cleanup(location)

    def test_two_lambda_folders(self):
        location = self.build_locations('two_lambda_folders_s3_event_api_gateway')

        coordinator.find_resources_and_create_yaml_template(location.project, None, False)

        self.assert_result_equal_to_expected(location)

        self.cleanup(location)

    def build_locations(self, name):
        project_location = '{}/{}'.format(self.tests_location, name)
        expected_template = '{}/{}.yaml'.format(self.templates, name)
        result_template = '{}/{}/template.yaml'.format(self.tests_location, name)

        return Location(project_location, expected_template, result_template)

    def sort(self, yaml_dict):
        for key in yaml_dict.keys():
            if type(yaml_dict[key]) is list:
                yaml_list = yaml_dict[key]
                yaml_list.sort()

                for list_el in yaml_list:
                    if type(list_el) is dict:
                        self.sort(list_el)
            elif type(yaml_dict[key]) is dict:
                self.sort(yaml_dict[key])

    def assert_result_equal_to_expected(self, location):
        with open(location.result, 'r') as result_stream, open(location.expected, 'r') as expected_stream:
            compare = yaml.safe_load(expected_stream)
            result = yaml.safe_load(result_stream)

            self.sort(compare)
            self.sort(result)

            self.assertDictEqual(compare, result)

    @staticmethod
    def cleanup(location):
        os.remove(location.result)
