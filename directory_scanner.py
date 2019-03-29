import os
import re
from pathlib import Path

LANGUAGE_SUFFIXES = {
    'python3': '.py',
    'node': '.js'  # which version
}


def get_number_of_files_for(language, file_names):
    return len(list(x for x in file_names if x.endswith(language)))


def guess_language(location):
    all_files_with_a_suffix = list(str(x) for x in Path(location).rglob("*.*"))
    languages_with_counts = {k: get_number_of_files_for(v, all_files_with_a_suffix) for k, v in LANGUAGE_SUFFIXES.items()}
    language =  max(languages_with_counts, key=languages_with_counts.get)

    return language, LANGUAGE_SUFFIXES[language]


def find_directory(location, language_suffix):
    dirs = list([x for x in Path(location).iterdir() if x.is_dir()])
    lambdas = []

    for a_dir in dirs:
        for file in list(a_dir.glob('*' + language_suffix)):  # should be language
            with file.open() as opened_file:
                regex = re.compile(r'.*def.*handler.\(*event.*context\)')
                result = list(filter(regex.search, opened_file.readlines()))

                if result:
                    file_name = os.path.relpath(str(file), str(a_dir))
                    dir_name = os.path.relpath(str(a_dir), location)
                    handler = build_handler(result, file_name)

                    lambdas.append({'name': dir_name, 'handler': handler, 'uri': dir_name})
    return lambdas


def build_handler(result, file_name):
    name = result[0]
    function_name = name[name.index('def') + 4:name.index('(')]
    file_name = file_name[0:file_name.index('.')]

    return '{}.{}'.format(file_name, function_name)



# print(find_directory('/Users/samvanovermeire/Documents/transcription-backend/', '.py'))
# guess_language('/Users/samvanovermeire/Documents/transcription-backend/')
