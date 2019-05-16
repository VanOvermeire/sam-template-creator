from typing import List

from template_creator.reader.strategies.PythonStrategy import PythonStrategy
from template_creator.reader.strategies.GoStrategy import GoStrategy
from template_creator.util.template_errors import LanguageError

STRATEGIES = {
    'python3.7|python3.6|python2.7': PythonStrategy,
    'go1.x': GoStrategy
    # java8
    # nodejs8.10 nodejs6.10
}


def build_strategy(language: str):
    for strategy in STRATEGIES.keys():
        if language in strategy:
            return STRATEGIES[strategy]()
    raise LanguageError('Could not find strategy for {}'.format(language))


def is_handler_file_for(language: str, lines: List[str]):
    for strategy in STRATEGIES.keys():
        if language in strategy:
            return STRATEGIES[strategy].is_handler_file(lines)
