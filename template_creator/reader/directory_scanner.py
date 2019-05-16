from pathlib import Path

from typing import List

from template_creator.util.constants import LANGUAGES_WITH_SUFFIXES
from template_creator.reader.strategies import language_strategy_builder
from template_creator.reader.FileInfo import FileInfo


def get_number_of_files_for(language_suffix: str, file_names: List[str]):
    return len(list(x for x in file_names if x.endswith(language_suffix)))


def executables_in_dir(a_dir, strategy):
    executables = list(a_dir.glob(strategy.get_executable_glob()))

    if len(executables) == 1:
        return str(executables[0])
    return None


def guess_language(location: str) -> str:
    all_files_with_a_suffix = list(str(x) for x in Path(location).rglob("*.*"))
    languages_with_counts = {k: get_number_of_files_for(v, all_files_with_a_suffix) for k, v in LANGUAGES_WITH_SUFFIXES.items()}
    language = max(languages_with_counts, key=languages_with_counts.get)

    return language


# could be recursive, for now just direct 'links' to other files (less complex)
def find_invoked_files(dirs, handler_file_lines, strategy, language_suffix) -> list:
    lines = []
    dirs_with_files = strategy.find_invoked_files(handler_file_lines)

    for a_dir in dirs:
        if a_dir.name in dirs_with_files.keys():
            filename = dirs_with_files[a_dir.name]

            for file in list(a_dir.glob('*{}'.format(language_suffix))):
                if filename == '*' or filename == file.name.replace(language_suffix, ''):
                    with file.open() as opened_file:
                        lines.extend(opened_file.readlines())
    return lines


def find_lambda_files_in_directory(location: str, language: str) -> List[dict]:
    lambdas = []
    dirs = list([x for x in Path(location).iterdir() if x.is_dir()])

    language_suffix = LANGUAGES_WITH_SUFFIXES[language]

    for a_dir in dirs:
        for file in list(a_dir.glob('*{}'.format(language_suffix))):
            with file.open() as opened_file:
                lines = opened_file.readlines()
                true, handler_line = language_strategy_builder.is_handler_file_for(language, lines)

                if true:
                    strategy = language_strategy_builder.build_strategy(language)
                    executable = executables_in_dir(a_dir, strategy)
                    other_file_lines = find_invoked_files(dirs, lines, strategy, language_suffix)
                    file_info = FileInfo(location, a_dir, file, handler_line, lines, strategy, other_file_lines, executable)

                    lambdas.append(file_info.build())
    return lambdas
