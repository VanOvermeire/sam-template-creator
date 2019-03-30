import os
from time import time

# TODO add other runtimes
RUNTIMES = ['python3.7', 'nodejs8.10']


def build_backup_name(template_name):
    first_part_of_name = template_name[0:template_name.index('.')]
    second_part_of_name = template_name[template_name.index('.'):len(template_name)]
    return '{}-{}{}'.format(first_part_of_name, int(time()), second_part_of_name)


def check_template_name(location, template_name):
    if template_name in os.listdir(location):
        backup_name = build_backup_name(template_name)
        print('{} is already in use, changing that file name to {}'.format(template_name, backup_name))
        os.rename('{}/{}'.format(location, template_name), '{}/{}'.format(location, backup_name))


def check_runtime(language):
    if language not in RUNTIMES:
        print('language {} not in list {}'.format(language, RUNTIMES))
        return False
    return True
