from ruamel.yaml import YAML

from constants.constants import EVENT_TYPES


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


def create_role_name(lambda_name):
    return '{}Role'.format(lambda_name)


def create_event_name(lambda_name, event):
    return '{}{}Event'.format(lambda_name, event)


def write_resources(lambdas):
    resources = dict()

    for l in lambdas:
        resources[l['name']] = create_lambda_function(l['name'], l['handler'], l['uri'], l['variables'], l['events'])
    # nicer effect when we loop again (all roles at the end of the template)
    for l in lambdas:
        resources[create_role_name(l['name'])] = create_role(l['permissions'])

    return {
        'Resources': resources
    }


def create_lambda_function(name, handler, uri, variables, events):
    generic = {
        'Type': 'AWS::Serverless::Function',
        'Properties': {
            'CodeUri': uri,
            'Handler': handler,
            'Role': '!GetAtt {}.Arn'.format(create_role_name(name)),
        }
    }

    add_variables(generic, variables)
    add_events(events, generic, name)

    return generic


def add_events(events, generic, name):
    events_with_value = dict()
    for event in events:
        events_with_value[create_event_name(name, event)] = EVENT_TYPES[event]
    if events_with_value:
        generic['Properties'].update({'Events': events_with_value})


def add_variables(generic, variables):
    variables_with_value = dict()
    for variable in variables:
        variables_with_value[variable] = 'Fill in value or delete if not needed'
    if variables_with_value:
        generic['Properties'].update({'Environment': variables_with_value})


def create_role(permissions):
    actions = ['logs:CreateLogStream', 'logs:CreateLogGroup', 'logs:PutLogEvents']
    actions.extend(permissions)

    return {
        'Type': 'AWS::IAM::Role',
        'Properties': {
            'AssumeRolePolicyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Principal': {
                            'Service': ['lambda.amazonaws.com']
                        },
                        'Action': ['sts:AssumeRole']
                    }
                ]
            },
            'Path': '"/',
            'Policies': [
                {
                    'PolicyName': 'LambdaPolicy',
                    'PolicyDocument': {
                        'Version': '2012-10-17',
                        'Statement': [
                            {
                                'Effect': 'Allow',
                                'Action': actions,
                                'Resource': '*'
                            }

                        ]
                    }
                }
            ]
        }
    }


def write(config):
    yaml = YAML()

    with open(config['location'], 'w') as yamlFile:
        complete_dict = write_header()
        complete_dict.update(write_global_section(config['language'], config['memory'], config['timeout']))
        complete_dict.update(write_resources(config['lambdas']))

        yaml.dump(complete_dict, yamlFile)
