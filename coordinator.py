from read import directory_scanner
from write import yaml_writer

# location = '/Users/samvanovermeire/Documents/transcription-backend/'  # temp

DEFAULT_TEMPLATE_NAME = 'temp-template.yaml'  # TODO change


def create_template(location):
    # checks.check_template_name(location, DEFAULT_TEMPLATE_NAME)
    language, suffix = directory_scanner.guess_language(location)
    lambdas = directory_scanner.find_directory(location, suffix)

    yaml_writer.write({'language': language, 'lambdas': lambdas, 'template': DEFAULT_TEMPLATE_NAME})  # TODO create file in location... and change the print
    print('Finished writing template to {}'.format(DEFAULT_TEMPLATE_NAME))
