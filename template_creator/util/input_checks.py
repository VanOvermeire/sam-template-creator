from pathlib import Path
import logging
from template_creator.util.constants import LANGUAGES_WITH_SUFFIXES

prefix = 'Failed to run tool:'


def check_runtime(language: str) -> bool:
    if language is not None and language not in LANGUAGES_WITH_SUFFIXES.keys():
        logging.error('language {} not in list {}'.format(language, LANGUAGES_WITH_SUFFIXES.keys()))
        return False
    return True


def check_location(location: str) -> bool:
    dirs = list([x for x in Path(location).iterdir() if x.is_dir()])

    if not len(dirs):
        logging.error('location {} does not contain any directories to search'.format(location))
        return False
    return True


def config_checks(location: str, language: str) -> bool:
    return check_runtime(language) and check_location(location)
