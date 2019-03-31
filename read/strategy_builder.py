from read.PythonStrategy import PythonStrategy


def build_strategy(language):
    if language == 'python3.7' or language == 'python3.6' or language == 'python2.7':
        return PythonStrategy()
    # other language strategies
    raise Exception('Could not find strategy for {}'.format(language))
