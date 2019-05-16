import re

from template_creator.reader.config.iam_config import GO_EXCEPTIONS
from template_creator.reader.strategies.language_strategy_common import find_variables_in_line_of_code, find_api, find_events


class GoStrategy:
    def build_handler(self, directory, file, handler_line, executable):
        if executable:
            return executable.rsplit('/', 1)[1]
        return 'handler'

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

    def find_permissions(self, lines):
        clients = set()
        regex = re.compile(r'.*github.com/aws/aws-sdk-go/service/.*')
        results = list(filter(regex.search, lines))

        for result in results:
            client = result.replace('github.com/aws/aws-sdk-go/service/', '').replace('"', '').strip()

            if '/' in client:
                client = client[:client.find('/')]

            if client in GO_EXCEPTIONS:
                client = GO_EXCEPTIONS[client]

            clients.add('{}:*'.format(client))

        return list(clients)

    @staticmethod
    def is_handler_file(lines):
        regex = re.compile(r'\s*lambda.Start\(')
        result = list(filter(regex.search, lines))

        if result:
            first_result = result[0]
            function_name = first_result[first_result.index('lambda.Start(') + 13: first_result.index(')')]

            return True, [line for line in lines if function_name in line][0]

        return False, None

    @staticmethod
    def find_invoked_files(handler_file_lines):
        lines_without_comments = [x for x in handler_file_lines if not x.strip().startswith('//')]
        results = dict()
        i = 0

        while i < len(lines_without_comments):
            line = lines_without_comments[i].strip()

            if line.startswith('import "'):
                import_statement = line.replace('import', '')
                result = import_statement[import_statement.find('"'):import_statement.rfind('"')]
                GoStrategy.__add_if_not_system_or_github(result, results)

            elif line.startswith('import ('):
                if '"' in line:
                    import_statement = line.replace('import (', '')
                    result = import_statement[import_statement.find('"'):import_statement.rfind('"')]
                    GoStrategy.__add_if_not_system_or_github(result, results)

                while ')' not in line:
                    line = lines_without_comments[i].strip()

                    if '"' in line:
                        result = line[line.find('"'):line.rfind('"')]
                        GoStrategy.__add_if_not_system_or_github(result, results)

                    i += 1

            i += 1

        return results

    @staticmethod
    def __add_if_not_system_or_github(result, results):
        if '/' in result and 'github.com' not in result:
            result = result[result.find('/') + 1:]
            results[result] = '*'

    @staticmethod
    def get_executable_glob():
        return '**/main'

    def __repr__(self):
        return self.__class__.__name__
