from read.PythonStrategy import PythonStrategy


def build_strategy(language):
    if language == 'python3.7':
        return PythonStrategy()
    # other language strategies
    raise Exception('Could not find strategy for {}'.format(language))
