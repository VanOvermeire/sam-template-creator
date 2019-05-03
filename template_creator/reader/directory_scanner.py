from pathlib import Path

from template_creator.util.constants import LANGUAGES_WITH_SUFFIXES
from template_creator.reader import language_strategy_builder
from template_creator.reader.FileInfo import FileInfo


def get_number_of_files_for(language_suffix, file_names):
    return len(list(x for x in file_names if x.endswith(language_suffix)))


def zip_in_dir(a_dir):
    zips = list(a_dir.glob('*.zip'))

    if len(zips) == 1:
        zip_file = str(zips[0])
        return zip_file.rsplit('/', 1)[1]
    return None


def guess_language(location):
    all_files_with_a_suffix = list(str(x) for x in Path(location).rglob("*.*"))
    languages_with_counts = {k: get_number_of_files_for(v, all_files_with_a_suffix) for k, v in LANGUAGES_WITH_SUFFIXES.items()}
    language = max(languages_with_counts, key=languages_with_counts.get)

    return language


def find_lambda_files_in_directory(location, language):
    dirs = list([x for x in Path(location).iterdir() if x.is_dir()])
    lambdas = []

    for a_dir in dirs:
        for file in list(a_dir.glob('*' + LANGUAGES_WITH_SUFFIXES[language])):
            with file.open() as opened_file:
                lines = opened_file.readlines()
                true, handler_line = language_strategy_builder.is_handler_file_for(language, lines)

                if true:
                    zip_file = zip_in_dir(a_dir)
                    strategy = language_strategy_builder.build_strategy(language)
                    file_info = FileInfo(location, a_dir, file, handler_line, lines, strategy, zip_file)
                    lambdas.append(file_info.build())
    return lambdas
