from ruamel.yaml import YAML


def write_header():
    return {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Transform': 'AWS::Serverless-2016-10-31'
    }


def write_global_section(language):
    return {
        'Globals': {
            'Function': {
                'Timeout': 3,
                'Runtime': language,
                'MemorySize': 512
            }
        }
    }


def write_resources(functions):
    resources = dict()

    for name, function in functions:
        resources[name] = function

    return {
        'Resources': resources
    }


def create_lambda_function_with_name(name, handler, uri, variables):
    return name, create_lambda_function(handler, uri, variables)


# TODO Role? -> try to find out and use built-in roles; Environment -> try to find out?; Events? Ignore others for now, later add options, maybe also something for api
def create_lambda_function(handler, uri, variables):
    variables_with_value = dict()

    for variable in variables:
        variables_with_value[variable] = 'FILL IN VALUE!'

    return {
        'Type': 'AWS::Serverless::Function',
        'Properties': {
            'CodeUri': uri,
            'Handler': handler,
            'Environment': {'Variables': variables_with_value}
        }
    }


def write(config):
    yaml = YAML()

    with open(config['location'], 'w') as yamlFile:
        complete_dict = write_header()
        complete_dict.update(write_global_section(config['language']))

        lambdas = []

        for l in config['lambdas']:
            lambdas.append(create_lambda_function_with_name(l['name'], l['handler'], l['uri'], l['variables']))

        complete_dict.update(write_resources(lambdas))

        yaml.dump(complete_dict, yamlFile)
