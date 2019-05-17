import os

from template_creator.util import template_checks
from template_creator.reader import directory_scanner
from template_creator.writer import yaml_writer
from template_creator.middleware import transformer

DEFAULT_TEMPLATE_NAME = 'template.yaml'


def find_full_path_for_yaml_template(location: str, template_name: str) -> str:
    if location.endswith('/'):
        return '{}{}'.format(location, template_name)
    return '{}/{}'.format(location, template_name)


def set_default_if_needed_for(language: str, location: str) -> str:
    if language is None:
        language = directory_scanner.guess_language(location)
        print('Language argument was not set. Found {}'.format(language))
    return language


def find_resources_and_create_yaml_template(location: str, language: str, set_global: bool) -> None:
    location = os.path.abspath(location)
    template_checks.check_template_name(location, DEFAULT_TEMPLATE_NAME)

    language = set_default_if_needed_for(language, location)
    template_location = find_full_path_for_yaml_template(location, DEFAULT_TEMPLATE_NAME)

    lambdas = directory_scanner.find_lambda_files_in_directory(location, language)

    if not lambdas:
        print('No lambdas found in {}'.format(location))
    else:
        other_resources = transformer.create_additional_resources(lambdas)

        yaml_writer.write({'language': language,
                           'lambdas': lambdas,
                           'other_resources': other_resources,
                           'location': template_location,
                           'set-global': set_global,
                           })

        print('Finished writing to {}. Check the template, there may be some things for you to fill in or edit.'.format(template_location))
