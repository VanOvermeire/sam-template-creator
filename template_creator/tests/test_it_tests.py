import os
import unittest

from ruamel import yaml

from template_creator import coordinator


class ITTests(unittest.TestCase):

    def setUp(self) -> None:
        self.tests_location = 'it-tests'
        self.templates = 'it-tests/templates'

    def test_one_lambda_basic_permissions(self):
        # TODO codeuri is generated as ./ Which should work, but could be cleaner without the /
        name = 'one_lambda_basic_permissions'

        project_location = '{}/{}'.format(self.tests_location, name)
        result_template_location = '{}/{}/template.yaml'.format(self.tests_location, name)
        template_location = '{}/{}.yaml'.format(self.templates, name)

        coordinator.find_resources_and_create_yaml_template(project_location, None, False)

        with open(result_template_location, 'r') as result_stream, open(template_location, 'r') as compare_stream:
            compare = yaml.safe_load(compare_stream)
            result = yaml.safe_load(result_stream)

            self.assertDictEqual(compare, result)

        os.remove(result_template_location)
