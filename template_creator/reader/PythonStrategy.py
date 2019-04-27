import os
import re

from template_creator.util.constants import EVENT_TYPES, HTTP_METHODS
from template_creator.reader.config.python_iam_config import EXCEPTIONS


class PythonStrategy:
    def build_handler(self, directory, file, handler_line):
        file_name = os.path.relpath(file, directory)
        function_name = handler_line[handler_line.index('def') + 4:handler_line.index('(')]
        file_name = file_name[0:file_name.index('.')]

        return '{}.{}'.format(file_name, function_name)

    def find_events(self, handler_line):
        try:
            lambda_event = handler_line[handler_line.index('(') + 1:handler_line.index('context)')]

            for event in EVENT_TYPES.keys():
                if event.lower() in lambda_event.lower():
                    return [event]
        except ValueError:
            return None

    def find_api(self, handler_line):
        method = []
        path = ''

        handler_prefix = handler_line[handler_line.index('def') + 4:handler_line.index('handler(')]
        split_prefix = list(map(lambda x: x.lower(), handler_prefix.split('_')))

        for line in split_prefix:
            if line in HTTP_METHODS:
                method = [line]
            elif len(line) > 0:
                path = '{}/{}'.format(path, line)

        if len(method) and len(path):
            method.append(path)

        return method

    # TODO selection too simple, might not work in more complex situations
    #  - for example, os.environ[BUCKET] where BUCKET is a variable name
    #  - ' vs "
    #  similar safety improvements for other methods here
    def find_env_variables(self, lines):
        variables = set()
        first_regex = re.compile(r'.*os.environ\[.*')
        second_regex = re.compile(r'.*os.environ.get\(.*')
        first_regex_results = list(filter(first_regex.search, lines))
        second_regex_results = list(filter(second_regex.search, lines))

        for result in first_regex_results:
            location_first_env_var = result.find('os.environ')

            while location_first_env_var != -1:
                result_start_from_loc = result[location_first_env_var:]
                variable = result_start_from_loc[12: result_start_from_loc.index(']') - 1]
                variables.add(variable)
                location_first_env_var = result.find('os.environ', location_first_env_var + 1)

        for result in second_regex_results:
            location_first_env_var = result.find('os.environ.get')

            while location_first_env_var != -1:
                result_start_from_loc = result[location_first_env_var:]
                variable = result_start_from_loc[16: result_start_from_loc.index(')') - 1]
                variables.add(variable)
                location_first_env_var = result.find('os.environ.get', location_first_env_var + 1)

        return list(variables)

    def find_role(self, lines):
        clients = set()
        regex = re.compile(r'.*boto3.client.*')
        results = list(filter(regex.search, lines))

        for result in results:
            client = result[result.index('boto3.client(\'') + 14: result.index('\')')]

            if client in EXCEPTIONS:
                client = EXCEPTIONS[client]

            clients.add('{}:*'.format(client))

        return list(clients)

    @staticmethod
    def is_handler_file(lines):
        regex = re.compile(r'\s*def\s.*handler.*\(.*event, context\)')
        result = list(filter(regex.search, lines))

        if result:
            return True, result[0]
        return False, None

    def __repr__(self):
        return self.__class__.__name__
