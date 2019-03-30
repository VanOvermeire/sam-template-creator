from ruamel.yaml import YAML


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


def write_resources(lambdas):
    resources = dict()

    for l in lambdas:
        resources[l['name']] = create_lambda_function(l['name'], l['handler'], l['uri'], l['variables'])
    # nicer effect when we loop again (all roles at the end of the template)
    for l in lambdas:
        resources[create_role_name(l['name'])] = create_role(l['permissions'])

    return {
        'Resources': resources
    }


def create_lambda_function(name, handler, uri, variables):
    variables_with_value = dict()

    for variable in variables:
        variables_with_value[variable] = 'FILL IN VALUE!'

    return {
        'Type': 'AWS::Serverless::Function',
        'Properties': {
            'CodeUri': uri,
            'Handler': handler,
            'Environment': {'Variables': variables_with_value},
            'Role': '!GetAtt {}.Arn'.format(create_role_name(name))
        }
    }


def create_role(permissions):
    actions = ['logs:CreateLogStream', 'logs:CreateLogGroup', 'logs:PutLogEvents']
    actions.extend(permissions)
    role = {
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

    return role


def write(config):
    yaml = YAML()

    with open(config['location'], 'w') as yamlFile:
        complete_dict = write_header()
        complete_dict.update(write_global_section(config['language'], config['memory'], config['timeout']))
        complete_dict.update(write_resources(config['lambdas']))

        yaml.dump(complete_dict, yamlFile)
