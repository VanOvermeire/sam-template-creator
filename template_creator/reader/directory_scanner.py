import logging
from pathlib import Path

from typing import List

from template_creator.util.constants import LANGUAGES_WITH_SUFFIXES
from template_creator.reader.strategies import language_strategy_builder
from template_creator.reader.FileInfo import FileInfo


def find_all_non_hidden_dirs(location):
    return list([x for x in Path(location).iterdir() if x.is_dir() and not x.name.startswith('.')])


def find_all_non_hidden_files_and_dirs(location):
    return list([x for x in Path(location).iterdir() if not x.name.startswith('.')])


def get_number_of_files_for(language_suffix: str, file_names: List[str]):
    return len(list(x for x in file_names if x.endswith(language_suffix)))


def executables_in_dir(a_dir, strategy):
    executables = list(a_dir.glob(strategy.get_executable_glob()))

    if len(executables) == 1:
        logging.debug('Found an executable in dir {}'.format(a_dir.name))
        return str(executables[0])
    return None


def guess_language(location: str) -> str:
    all_files_with_a_suffix = list(str(x) for x in Path(location).rglob("*.*"))
    languages_with_counts = {k: get_number_of_files_for(v, all_files_with_a_suffix) for k, v in LANGUAGES_WITH_SUFFIXES.items()}
    language = max(languages_with_counts, key=languages_with_counts.get)

    return language


# TODO could be recursive, for now just direct 'links' to other files (less complex)
# start with root and check files there as well?
def find_invoked_files(dirs, handler_file_lines, strategy, language_suffix) -> list:
    lines = []
    dirs_with_files = strategy.find_invoked_files(handler_file_lines)

    for a_dir in dirs:
        if a_dir.name in dirs_with_files.keys():
            filename = dirs_with_files[a_dir.name]

            for file in list(a_dir.glob('*{}'.format(language_suffix))):
                if filename == '*' or filename == file.name.replace(language_suffix, ''):
                    logging.debug('Found file that was called by our handler file: {}'.format(file.name))
                    with file.open() as opened_file:
                        lines.extend(opened_file.readlines())
    return lines


def find_lambda_files_in_directory(location: str, language: str, current_dir=None, root_dirs=None) -> List[dict]:
    lambdas = []

    if not current_dir and not root_dirs:
        current_dir = Path(location)
        root_dirs = find_all_non_hidden_dirs(location)
        dirs_and_files = find_all_non_hidden_files_and_dirs(location)
    else:
        dirs_and_files = find_all_non_hidden_files_and_dirs(current_dir)

    for df in dirs_and_files:
        logging.debug('Checking {}'.format(df))
        if df.is_dir():
            lambdas.extend(find_lambda_files_in_directory(location, language, df, root_dirs))
        else:
            result, file_info_build = check_language_file_for_lambda(df, current_dir, root_dirs, location, language)

            if result:
                lambdas.append(file_info_build)
    return lambdas


def check_language_file_for_lambda(file, current_dir, root_dirs, location, language):
    logging.debug('Checking file {}'.format(file.name))
    language_suffix = LANGUAGES_WITH_SUFFIXES[language]

    if file.name.endswith(language_suffix):
        with file.open() as opened_file:
            lines = opened_file.readlines()
            true, handler_line = language_strategy_builder.is_handler_file_for(language, lines)

            if true:
                logging.debug('Found handler file {} in dir {}'.format(file.name, current_dir.name))
                strategy = language_strategy_builder.build_strategy(language)
                executable = executables_in_dir(current_dir, strategy)
                other_file_lines = find_invoked_files(root_dirs, lines, strategy, language_suffix)
                file_info = FileInfo(location, current_dir, file, handler_line, lines, strategy, other_file_lines, executable)
                logging.debug('Building file info {} and adding to array'.format(file_info))

                return True, file_info.build()
    return False, None
