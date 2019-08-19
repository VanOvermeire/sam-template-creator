import logging

from typing import List

from template_creator.util.constants import EVENT_TYPES

SCHEDULE_WITH_RATE_PREFIX = 'Schedule:'


def create_lambda_function(name: str, handler: str, uri: str, variables, events, api, existing_template) -> dict:
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
    existing_variables = find_existing_env_var_values(existing_template)
    _add_variables(generic, variables, existing_variables)
    _add_events(generic, events, name)
    _add_api(generic, api)

    return generic


def create_event_name(lambda_name: str, event: str) -> str:
    return '{}{}Event'.format(lambda_name, event)


def create_role_name(lambda_name: str) -> str:
    return '{}Role'.format(lambda_name)


def _add_events(generic: dict, events: List[str], name: str) -> None:
    events_with_value = dict()
    if events:
        for event in events:
            if SCHEDULE_WITH_RATE_PREFIX in event:
                schedule_event = EVENT_TYPES['Schedule']
                schedule_event['Properties']['Schedule'] = 'rate({})'.format(event.replace(SCHEDULE_WITH_RATE_PREFIX, ''))
                events_with_value[create_event_name(name, 'Schedule')] = schedule_event
            else:
                events_with_value[create_event_name(name, event)] = EVENT_TYPES[event]

        generic['Properties'].update({'Events': events_with_value})


def _add_variables(generic: dict, variables: List[str], existing_variables) -> None:
    variables_with_value = dict()

    if variables:
        for variable in variables:
            if variable in existing_variables:  # this kind of logic *might* also fit in with the transformer, but ok for now
                logging.info('Value for environment variable {} found in existing template: {}. Adding to new template'.format(variable, existing_variables[variable]))
                variables_with_value[variable] = existing_variables[variable]
            else:
                variables_with_value[variable] = 'Fill in value or delete if not needed'

        generic['Properties'].update({
            'Environment': {
                'Variables': variables_with_value
            }
        })


def find_existing_env_var_values(existing_template):
    names_of_variables = {}

    if 'Resources' in existing_template:
        for name, value in existing_template['Resources'].items():
            if value['Type'] == 'AWS::Serverless::Function':
                try:
                    # will overwrite existing keys, probably ok behavior
                    names_of_variables.update(value['Properties']['Environment']['Variables'])
                except KeyError:
                    pass

    return names_of_variables


def _add_api(generic: dict, api: List[str]) -> None:
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


def create_role(name: str, permissions: List[str]) -> (str, dict):
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
