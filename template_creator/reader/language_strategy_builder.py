from template_creator.reader.PythonStrategy import PythonStrategy
from template_creator.util.template_errors import LanguageError

STRATEGIES = {
    'python3.7|python3.6|python2.7': PythonStrategy
    # other languages, like node
}


def build_strategy(language):
    for strategy in STRATEGIES.keys():
        if language in strategy:
            return STRATEGIES[strategy]()
    raise LanguageError('Could not find strategy for {}'.format(language))


def is_handler_file_for(language, lines):
    for strategy in STRATEGIES.keys():
        if language in strategy:
            return STRATEGIES[strategy].is_handler_file(lines)
