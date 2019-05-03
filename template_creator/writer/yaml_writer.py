from ruamel.yaml import YAML

from template_creator.writer import lambda_writer
from template_creator.writer import header_writer


def write_lambdas(lambdas, no_globals, language, memory, timeout):
    resources = dict()

    for l in lambdas:
        new_lambda = lambda_writer.create_lambda_function(l['name'], l['handler'], l['uri'], l['variables'], l['events'], l['api'])

        if no_globals:
            new_lambda['Properties']['Timeout'] = timeout
            new_lambda['Properties']['Runtime'] = language
            new_lambda['Properties']['MemorySize'] = memory

        resources[l['name']] = new_lambda

    return resources


def write_roles(lambdas):
    resources = dict()

    for l in lambdas:
        name, role = lambda_writer.create_role(l['name'], l['permissions'])
        resources[name] = role

    return resources


def write_all_resources(config):
    resources = dict()

    resources.update(write_lambdas(config['lambdas'], config['no-globals'], config['language'], config['memory'], config['timeout']))
    resources.update(write_roles(config['lambdas']))
    resources.update(config['other_resources'])

    return {
        'Resources': resources
    }


def write(config):
    yaml = YAML()
    yaml.Representer.ignore_aliases = lambda *args: True

    with open(config['location'], 'w') as yamlFile:
        complete_dict = {}
        complete_dict.update(header_writer.write_headers(config))
        complete_dict.update(write_all_resources(config))

        yaml.dump(complete_dict, yamlFile)
