from ruamel.yaml import YAML

from template_creator.writer import lambda_writer


def write_header():
    return {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Transform': 'AWS::Serverless-2016-10-31'
    }


def write_global_section(language, memory, timeout):
    return {
        'Globals': {
            'Function': {
                'Timeout': timeout,
                'Runtime': language,
                'MemorySize': memory
            }
        }
    }


def write_lambdas(lambdas):
    resources = dict()

    for l in lambdas:
        resources[l['name']] = lambda_writer.create_lambda_function(l['name'], l['handler'], l['uri'], l['variables'], l['events'], l['api'])

    return resources


def write_roles(lambdas):
    resources = dict()

    for l in lambdas:
        name, role = lambda_writer.create_role(l['name'], l['permissions'])
        resources[name] = role

    return resources


def write_all_resources(lambdas, other_resources):
    resources = dict()

    resources.update(write_lambdas(lambdas))
    resources.update(write_roles(lambdas))
    resources.update(other_resources)

    return {
        'Resources': resources
    }


def write(config):
    yaml = YAML()

    with open(config['location'], 'w') as yamlFile:
        complete_dict = write_header()
        complete_dict.update(write_global_section(config['language'], config['memory'], config['timeout']))
        complete_dict.update(write_all_resources(config['lambdas'], config['other_resources']))

        yaml.dump(complete_dict, yamlFile)
