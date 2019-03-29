from ruamel.yaml import YAML


def write_header():
    to_write = dict()
    to_write['AWSTemplateFormatVersion'] = '2010-09-09'
    to_write['Transform'] = 'AWS::Serverless-2016-10-31'

    return to_write


def write_global_section(language):
    to_write = dict()
    global_section = dict()

    function = dict()
    function['Timeout'] = 3
    function['Runtime'] = language
    function['MemorySize'] = 512
    global_section['Function'] = function

    to_write['Globals'] = global_section

    return to_write


def write_resources(functions):
    to_write = dict()
    resources = dict()

    for name, function in functions:
        resources[name] = function

    to_write['Resources'] = resources

    return to_write


def create_lambda_function_with_name(name, handler, uri):
    return name, create_lambda_function(handler, uri)


# TODO Role? -> try to find out and use built-in roles; Environment -> try to find out?; Events? Ignore others for now, later add options, maybe also something for api
# Runtime, Timeout = set globally
def create_lambda_function(handler, uri):
    return {
        'Type': 'AWS::Serverless::Function',
        'Properties': {
            'CodeUri': uri,
            'Handler': handler
        }
    }


# TODO should write to template.yaml, if it does not exist
def write(config):
    yaml = YAML()

    with open(config['template'], 'w') as yamlFile:
        complete_dict = write_header()
        complete_dict.update(write_global_section(config['language']))

        lambdas = []

        for l in config['lambdas']:
            lambdas.append(create_lambda_function_with_name(l['name'], l['handler'], l['uri']))

        complete_dict.update(write_resources(lambdas))

        yaml.dump(complete_dict, yamlFile)
