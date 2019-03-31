import re
from pathlib import Path

from constants.constants import LANGUAGES_WITH_SUFFIXES
from read import strategy_builder
from read.FileInfo import FileInfo


def get_number_of_files_for(language, file_names):
    return len(list(x for x in file_names if x.endswith(language)))


def guess_language(location):
    all_files_with_a_suffix = list(str(x) for x in Path(location).rglob("*.*"))
    languages_with_counts = {k: get_number_of_files_for(v, all_files_with_a_suffix) for k, v in LANGUAGES_WITH_SUFFIXES.items()}
    language = max(languages_with_counts, key=languages_with_counts.get)

    return language


# TODO this is part of the strategy as well, so should go somewhere else
def is_handler_file(lines):
    regex = re.compile(r'\s*def\s.*handler.*\(.*event, context\)')
    result = list(filter(regex.search, lines))

    if result:
        return True, result[0]
    return False, None


def find_directory(location, language):
    dirs = list([x for x in Path(location).iterdir() if x.is_dir()])
    lambdas = []

    for a_dir in dirs:
        for file in list(a_dir.glob('*' + LANGUAGES_WITH_SUFFIXES[language])):
            with file.open() as opened_file:
                lines = opened_file.readlines()
                true, handler_line = is_handler_file(lines)

                if true:
                    strategy = strategy_builder.build_strategy(language)
                    file_info = FileInfo(location, a_dir, file, handler_line, lines, strategy)
                    lambdas.append(file_info.build())
    return lambdas
