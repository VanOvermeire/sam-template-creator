from template_creator.util.constants import LANGUAGES_WITH_SUFFIXES


def check_runtime(language):
    if language is not None and language not in LANGUAGES_WITH_SUFFIXES.keys():
        print('language {} not in list {}'.format(language, list(LANGUAGES_WITH_SUFFIXES.keys())))
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
