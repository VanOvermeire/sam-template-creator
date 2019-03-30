from checks import checks
from read import directory_scanner
from write import yaml_writer

DEFAULT_TEMPLATE_NAME = 'template.yaml'


def full_location_template(location, template_name):
    if location.endswith('/'):
        return '{}{}'.format(location, template_name)
    return '{}/{}'.format(location, template_name)


def create_template(location):
    checks.check_template_name(location, DEFAULT_TEMPLATE_NAME)
    language, suffix = directory_scanner.guess_language(location)
    lambdas = directory_scanner.find_directory(location, suffix)
    template_location = full_location_template(location, DEFAULT_TEMPLATE_NAME)
    yaml_writer.write({'language': language, 'lambdas': lambdas, 'location': template_location})
    print('Finished writing template to {}'.format(template_location))
