from checks import checks
from read import directory_scanner
from write import yaml_writer
from middleware import transformer

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
    other_resources = transformer.add_to_resources(lambdas)

    template_location = full_location_template(location, DEFAULT_TEMPLATE_NAME)
    yaml_writer.write({'language': language, 'lambdas': lambdas, 'other_resources': other_resources,
                       'location': template_location, 'memory': memory, 'timeout': timeout})

    print('Finished writing to {}. Check the template, there may be some things for you to fill in or edit.'.format(template_location))
