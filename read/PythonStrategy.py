import os
import re

from constants.constants import EVENT_TYPES


class PythonStrategy:

    def build_handler(self, directory, file, handler_line):
        file_name = os.path.relpath(file, directory)
        function_name = handler_line[handler_line.index('def') + 4:handler_line.index('(')]
        file_name = file_name[0:file_name.index('.')]

        return '{}.{}'.format(file_name, function_name)

    # TODO for both of these, use set instead of array
    # TODO selection too simple, might not work in more complex situations
    #  - for example, os.environ[BUCKET] where BUCKET is a variable name
    def find_env_variables(self, lines):
        variables = []
        first_regex = re.compile(r'.*os.environ\[.*')
        second_regex = re.compile(r'.*os.environ.get\(.*')
        first_regex_results = list(filter(first_regex.search, lines))
        second_regex_results = list(filter(second_regex.search, lines))

        for result in first_regex_results:
            variable = result[result.index('os.environ[\'') + 12: result.index('\']')]
            variables.append(variable)

        for result in second_regex_results:
            variable = result[result.index('os.environ.get(\'') + 16: result.index('\')')]
            variables.append(variable)

        return variables

    def find_role(self, lines):
        clients = []
        regex = re.compile(r'.*boto3.client.*')
        results = list(filter(regex.search, lines))

        for result in results:
            client = result[result.index('boto3.client(\'') + 14: result.index('\')')]
            clients.append('{}:*'.format(client))  # TODO may not work for all clients

        return clients

    def find_events(self, handler_line):
        lambda_event = handler_line[handler_line.index('(') + 1:handler_line.index('context)')]

        for event in EVENT_TYPES.keys():
            if event.lower() in lambda_event.lower():
                return [event]
