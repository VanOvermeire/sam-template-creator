from template_creator.util.constants import LANGUAGES_WITH_SUFFIXES


def check_runtime(language):
    if language is not None and language not in LANGUAGES_WITH_SUFFIXES.keys():
        print('language {} not in list {}'.format(language, list(LANGUAGES_WITH_SUFFIXES.keys())))
        return False
    return True


def config_checks(language):
    return check_runtime(language)
