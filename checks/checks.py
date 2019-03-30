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
        print('{} is already in use, changing that file to {}'.format(template_name, backup_name))
        os.rename('{}/{}'.format(location, template_name), '{}/{}'.format(location, backup_name))


def check_runtime(language):
    if language is not None and language not in RUNTIMES:
        print('language {} not in list {}'.format(language, RUNTIMES))
        return False
    return True


def check_timeout(timeout):
    try:
        if timeout is not None and (int(timeout) < 1 or int(timeout) > 900):
            print('timeout {} is invalid (should be between 1 and 900)'.format(timeout))
            return False
    except ValueError:
        print('timeout {} is not a valid number'.format(timeout))
        return False
    return True


def check_memory(memory):
    try:
        if memory is not None and (int(memory) < 128 or int(memory) > 3008 or int(memory) % 2 != 0):
            print('memory {} is invalid (should be between 128 and 3008)'.format(memory))
            return False
    except ValueError:
        print('memory {} is not a valid number'.format(memory))
        return False
    return True


def config_checks(language, timeout, memory):
    return check_runtime(language) and check_timeout(timeout) and check_memory(memory)
