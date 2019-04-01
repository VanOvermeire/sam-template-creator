from read.PythonStrategy import PythonStrategy

STRATEGIES = {
    'python3.7|python3.6|python2.7': PythonStrategy
    # other languages, like node
}


def build_strategy(language):
    for strategy in STRATEGIES.keys():
        if language in strategy:
            return STRATEGIES[strategy]()
    raise Exception('Could not find strategy for {}'.format(language))


def is_handler_file_for(language, lines):
    for strategy in STRATEGIES.keys():
        if language in strategy:
            return STRATEGIES[strategy].is_handler_file(lines)
