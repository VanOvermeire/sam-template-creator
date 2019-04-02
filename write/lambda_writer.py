from constants.constants import EVENT_TYPES


def create_lambda_function(name, handler, uri, variables, events, api):
    generic = {
        'Type': 'AWS::Serverless::Function',
        'Properties': {
            'CodeUri': uri,
            'Handler': handler,
            'Role': {
                'Fn::GetAtt': [
                    create_role_name(name),
                    'Arn'
                ]
            }
        }
    }

    add_variables(generic, variables)
    add_events(generic, events, name)
    add_api(generic, api)

    return generic


def create_event_name(lambda_name, event):
    return '{}{}Event'.format(lambda_name, event)


def create_role_name(lambda_name):
    return '{}Role'.format(lambda_name)


def add_events(generic, events, name):
    events_with_value = dict()
    if events:
        for event in events:
            events_with_value[create_event_name(name, event)] = EVENT_TYPES[event]

        generic['Properties'].update({'Events': events_with_value})


def add_variables(generic, variables):
    variables_with_value = dict()

    if variables:
        for variable in variables:
            variables_with_value[variable] = 'Fill in value or delete if not needed'

        generic['Properties'].update({
            'Environment': {
                'Variables': variables_with_value
            }
        })


def add_api(generic, api):
    if api:
        method = api[0]
        path = api[1]

        generic['Properties'].update({
            'Events': {
                method.upper(): {
                    'Type': 'Api',
                    'Properties': {
                        'Path': path,
                        'Method': method
                    }
                }
            }
        })


def create_role(name, permissions):
    role_name = create_role_name(name)
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
            'Path': '/',
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
    return role_name, role
