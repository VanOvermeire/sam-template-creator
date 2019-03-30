from checks import checks
from read import directory_scanner
from write import yaml_writer

DEFAULT_TEMPLATE_NAME = 'template.yaml'


def full_location_template(location, template_name):
    if location.endswith('/'):
        return '{}{}'.format(location, template_name)
    return '{}/{}'.format(location, template_name)


def create_template(location, language, timeout, memory):
    checks.check_template_name(location, DEFAULT_TEMPLATE_NAME)

    if language is None:
        language = directory_scanner.guess_language(location)
    if timeout is None:
        timeout = 3
    if memory is None:
        memory = 512

    lambdas = directory_scanner.find_directory(location, language)

    template_location = full_location_template(location, DEFAULT_TEMPLATE_NAME)
    yaml_writer.write({'language': language, 'lambdas': lambdas, 'location': template_location, 'memory': memory, 'timeout': timeout})
    print('Finished writing template to {}'.format(template_location))
