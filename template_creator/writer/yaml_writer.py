from ruamel.yaml import YAML

from template_creator.writer import lambda_writer
from template_creator.writer import header_writer


def _write_lambdas(lambdas: list, set_globals: bool, language: str, existing_template: dict) -> dict:
    resources = dict()

    for l in lambdas:
        new_lambda = lambda_writer.create_lambda_function(l['name'], l['handler'], l['uri'], l['variables'], l['events'], l['api'], existing_template)

        if not set_globals:
            new_lambda['Properties']['Runtime'] = language
            new_lambda['Properties']['Timeout'] = 3
            new_lambda['Properties']['MemorySize'] = 512

        resources[l['name']] = new_lambda

    return resources


def _write_roles(lambdas: list) -> dict:
    resources = dict()

    for l in lambdas:
        name, role = lambda_writer.create_role(l['name'], l['permissions'])
        resources[name] = role

    return resources


def _write_all_resources(config: dict) -> dict:
    resources = dict()

    resources.update(_write_lambdas(config['lambdas'], config['set-global'], config['language'], config['existing_template']))
    resources.update(_write_roles(config['lambdas']))
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
        complete_dict.update(_write_all_resources(config))

        yaml.dump(complete_dict, yamlFile)
