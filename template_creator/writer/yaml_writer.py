from ruamel.yaml import YAML

from template_creator.writer import lambda_writer
from template_creator.writer import header_writer


def write_lambdas(lambdas: dict, set_globals: bool, language: str) -> dict:
    resources = dict()

    for l in lambdas:
        new_lambda = lambda_writer.create_lambda_function(l['name'], l['handler'], l['uri'], l['variables'], l['events'], l['api'])

        if not set_globals:
            new_lambda['Properties']['Runtime'] = language
            new_lambda['Properties']['Timeout'] = 3
            new_lambda['Properties']['MemorySize'] = 512

        resources[l['name']] = new_lambda

    return resources


def write_roles(lambdas: dict) -> dict:
    resources = dict()

    for l in lambdas:
        name, role = lambda_writer.create_role(l['name'], l['permissions'])
        resources[name] = role

    return resources


def write_all_resources(config: dict) -> dict:
    resources = dict()

    resources.update(write_lambdas(config['lambdas'], config['set-global'], config['language']))
    resources.update(write_roles(config['lambdas']))
    resources.update(config['other_resources'])

    return {
        'Resources': resources
    }


def write(config: dict) -> None:
    yaml = YAML()
    yaml.Representer.ignore_aliases = lambda *args: True

    with open(config['location'], 'w') as yamlFile:
        complete_dict = {}
        complete_dict.update(header_writer.write_headers(config))
        complete_dict.update(write_all_resources(config))

        yaml.dump(complete_dict, yamlFile)
