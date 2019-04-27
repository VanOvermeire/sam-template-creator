import re

from template_creator.reader.language_strategy_common import find_variables_in_line_of_code, find_api, find_events


class GoStrategy:
    def build_handler(self, directory, file, handler_line):
        return 'main'  # TODO check if this works

    def find_events(self, handler_line):
        try:
            lambda_full_event = handler_line[handler_line.index('Context, ') + 9:handler_line.index(')')]
            lambda_event = lambda_full_event[0:lambda_full_event.index(' ')]

            return find_events(lambda_event)
        except ValueError:
            return None

    def find_api(self, handler_line):
        try:
            handler_prefix = handler_line[handler_line.index('func ') + 5:handler_line.index('Request')]
            split_prefix = re.split('(?=[A-Z])', handler_prefix)

            return find_api(split_prefix)
        except ValueError:
            return []

    def find_env_variables(self, lines):
        variables = set()
        first_regex = re.compile(r'.*os.Getenv\(.*')
        first_regex_results = list(filter(first_regex.search, lines))

        for result in first_regex_results:
            variables.update(find_variables_in_line_of_code(result, 'os.Getenv(', ')'))

        return list(variables)

    def find_role(self, lines):
        clients = set()
        regex = re.compile(r'.*github.com/aws/aws-sdk-go/service/.*')
        results = list(filter(regex.search, lines))

        for result in results:
            client = result[result.rfind('/') + 1:result.rfind('"')]

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
