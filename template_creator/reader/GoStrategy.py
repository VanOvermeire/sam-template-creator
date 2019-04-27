import os
import re

from template_creator.util.constants import EVENT_TYPES, HTTP_METHODS
from template_creator.reader.config.python_iam_config import EXCEPTIONS


# potential code reuse (compare python strategy)
class GoStrategy:
    def build_handler(self, directory, file, handler_line):
        return 'main'  # TODO check if this works

    def find_events(self, handler_line):
        try:
            lambda_full_event = handler_line[handler_line.index('Context, ') + 9:handler_line.index(')')]
            lambda_event = lambda_full_event[0:lambda_full_event.index(' ')]

            for event in EVENT_TYPES.keys():
                if event.lower() in lambda_event.lower():
                    return [event]
        except ValueError:
            return None

    def find_api(self, handler_line):
        try:
            method = []
            path = ''

            handler_prefix = handler_line[handler_line.index('func ') + 5:handler_line.index('Request')]
            split_prefix = re.split('(?=[A-Z])', handler_prefix)

            for line in split_prefix:
                lowecase_line = line.lower()

                if lowecase_line in HTTP_METHODS:
                    method = [lowecase_line]
                elif len(lowecase_line) > 0:
                    path = '{}/{}'.format(path, lowecase_line)

            if len(method) and len(path):
                method.append(path)

            return method
        except ValueError:
            return []

    def find_env_variables(self, lines):
        variables = set()
        first_regex = re.compile(r'.*os.Getenv\(.*')
        first_regex_results = list(filter(first_regex.search, lines))

        for result in first_regex_results:
            location_first_env_var = result.find('os.Getenv("')
            # TODO move this while logic to helper (also see python strategy)
            while location_first_env_var != -1:
                result_start_from_loc = result[location_first_env_var:]
                variable = result_start_from_loc[11: result_start_from_loc.index('")')]
                variables.add(variable)
                location_first_env_var = result.find('os.Getenv', location_first_env_var + 1)

        return list(variables)

    def find_role(self, lines):
        clients = set()
        regex = re.compile(r'.*github.com/aws/aws-sdk-go/service/.*')
        results = list(filter(regex.search, lines))

        for result in results:
            print(result)
            client = result[result.rfind('/') + 1:result.rfind('"')]
            print(client)

            # TODO check exceptions
            # if client in EXCEPTIONS:
            #     client = EXCEPTIONS[client]

            clients.add('{}:*'.format(client))

        return list(clients)

    @staticmethod
    def is_handler_file(lines):
        regex = re.compile(r'\s*lambda.Start\(')
        result = list(filter(regex.search, lines))

        if result:
            first_result = result[0]
            function_name = first_result[first_result.index('lambda.Start(') + 13 : first_result.index(')')]

            return True, [line for line in lines if function_name in line][0]

        return False, None

    def __repr__(self):
        return self.__class__.__name__