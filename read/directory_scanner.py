import re
from pathlib import Path
from read.FileInfo import FileInfo

LANGUAGE_SUFFIXES = {
    'python3': '.py',
    'node': '.js'  # TODO which version?
}


def get_number_of_files_for(language, file_names):
    return len(list(x for x in file_names if x.endswith(language)))


def guess_language(location):
    all_files_with_a_suffix = list(str(x) for x in Path(location).rglob("*.*"))
    languages_with_counts = {k: get_number_of_files_for(v, all_files_with_a_suffix) for k, v in LANGUAGE_SUFFIXES.items()}
    language = max(languages_with_counts, key=languages_with_counts.get)

    return language, LANGUAGE_SUFFIXES[language]


def is_handler_file(lines):
    regex = re.compile(r'.*def.*handler.\(*event.*context\)')
    result = list(filter(regex.search, lines))

    if result:
        return True, result[0]
    return False, None


def find_directory(location, language_suffix):
    dirs = list([x for x in Path(location).iterdir() if x.is_dir()])
    lambdas = []

    for a_dir in dirs:
        for file in list(a_dir.glob('*' + language_suffix)):
            with file.open() as opened_file:
                lines = opened_file.readlines()
                true, handler_line = is_handler_file(lines)

                if true:
                    file_info = FileInfo(location, a_dir, file, handler_line, lines)
                    lambdas.append(file_info.build())
    return lambdas


# print(find_directory('/Users/samvanovermeire/Documents/transcription-backend/', '.py'))
# guess_language('/Users/samvanovermeire/Documents/transcription-backend/')
