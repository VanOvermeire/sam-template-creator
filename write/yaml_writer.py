from ruamel.yaml import YAML

from write import lambda_writer


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


def write_resources(lambdas):
    resources = dict()

    for l in lambdas:
        resources[l['name']] = lambda_writer.create_lambda_function(l['name'], l['handler'], l['uri'], l['variables'], l['events'])

    # TODO this kind of logic does not belong here. yaml writer has to write in the right way, not create new resources
    for l in lambdas:
        if 'S3' in l['events']:
            resources['S3EventBucket'] = {
                'Type': 'AWS::S3::Bucket'
            }
            break

    # nicer effect when we loop again (all roles at the end of the template)
    for l in lambdas:
        name, role = lambda_writer.create_role(l['name'], l['permissions'])
        resources[name] = role

    return {
        'Resources': resources
    }


def write(config):
    yaml = YAML()

    with open(config['location'], 'w') as yamlFile:
        complete_dict = write_header()
        complete_dict.update(write_global_section(config['language'], config['memory'], config['timeout']))
        complete_dict.update(write_resources(config['lambdas']))

        yaml.dump(complete_dict, yamlFile)
