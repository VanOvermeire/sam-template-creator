import logging
import os
from time import time
from ruamel import yaml


def build_backup_name(template_name: str) -> str:
    first_part_of_name = template_name[0:template_name.index('.')]
    second_part_of_name = template_name[template_name.index('.'):len(template_name)]
    return '{}-{}{}'.format(first_part_of_name, int(time()), second_part_of_name)


# TODO only return if it is a SAM template
def get_existing_template_as_dict(location: str, template_name: str) -> dict:
    with open('{}/{}'.format(location, template_name), 'r') as file_stream:
        return yaml.safe_load(file_stream)


def check_template_name(location: str, template_name: str) -> dict:
    if template_name in os.listdir(location):
        existing_template_as_dict = get_existing_template_as_dict(location, template_name)
        backup_name = build_backup_name(template_name)
        logging.info('{} is already in use, changing that file to {}'.format(template_name, backup_name))
        os.rename('{}/{}'.format(location, template_name), '{}/{}'.format(location, backup_name))

        return existing_template_as_dict
    return {}
