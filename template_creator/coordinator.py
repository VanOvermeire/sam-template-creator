import os

from template_creator.util import template_checks
from template_creator.reader import directory_scanner
from template_creator.writer import yaml_writer
from template_creator.middleware import transformer

DEFAULT_TEMPLATE_NAME = 'template.yaml'


def find_full_path_for_yaml_template(location, template_name):
    if location.endswith('/'):
        return '{}{}'.format(location, template_name)
    return '{}/{}'.format(location, template_name)


def set_defaults_if_needed(language, location, memory, timeout):
    if language is None:
        language = directory_scanner.guess_language(location)
    if timeout is None:
        timeout = 3
    if memory is None:
        memory = 512
    return language, memory, timeout


def find_resources_and_create_yaml_template(location, language, timeout, memory):
    location = os.path.abspath(location)
    template_checks.check_template_name(location, DEFAULT_TEMPLATE_NAME)

    language, memory, timeout = set_defaults_if_needed(language, location, memory, timeout)
    template_location = find_full_path_for_yaml_template(location, DEFAULT_TEMPLATE_NAME)

    lambdas = directory_scanner.find_lambda_files_in_directory(location, language)
    other_resources = transformer.add_to_resources(lambdas)

    yaml_writer.write({'language': language,
                       'lambdas': lambdas,
                       'other_resources': other_resources,
                       'location': template_location,
                       'memory': memory,
                       'timeout': timeout
                       })

    print('Finished writing to {}. Check the template, there may be some things for you to fill in or edit.'.format(template_location))
