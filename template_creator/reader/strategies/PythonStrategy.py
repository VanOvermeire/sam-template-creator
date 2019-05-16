import os
import re

from template_creator.reader.strategies.language_strategy_common import find_variables_in_line_of_code, find_api, find_events
from template_creator.reader.config.iam_config import PYTHON_EXCEPTIONS


class PythonStrategy:
    def build_handler(self, directory, file, handler_line, executable):
        file_name = os.path.relpath(file, directory)
        function_name = handler_line[handler_line.index('def') + 4:handler_line.index('(')]
        file_name = file_name[0:file_name.index('.')]

        return '{}.{}'.format(file_name, function_name)

    def find_events(self, handler_line):
        try:
            lambda_event = handler_line[handler_line.index('(') + 1:handler_line.index('context)')]

            return find_events(lambda_event)
        except ValueError:
            return None

    def find_api(self, handler_line):
        try:
            handler_prefix = handler_line[handler_line.index('def') + 4:handler_line.index('handler(')]
            split_prefix = list(map(lambda x: x.lower(), handler_prefix.split('_')))

            return find_api(split_prefix)
        except ValueError:
            return []

    # TODO selection too simple, might not work in more complex situations
    #  - for example, os.environ[BUCKET] where BUCKET is a variable name
    #  similar safety improvements for other methods here
    def find_env_variables(self, all_lines):
        variables = set()
        first_regex = re.compile(r'.*os.environ\[.*')
        second_regex = re.compile(r'.*os.environ.get\(.*')
        first_regex_results = list(filter(first_regex.search, all_lines))
        second_regex_results = list(filter(second_regex.search, all_lines))

        for result in first_regex_results:
            variables.update(find_variables_in_line_of_code(result, 'os.environ[', ']'))

        for result in second_regex_results:
            variables.update(find_variables_in_line_of_code(result, 'os.environ.get(', ')'))

        return list(variables)

    def find_permissions(self, all_lines):
        clients = set()
        regex = re.compile(r'.*boto3.client.*')
        results = list(filter(regex.search, all_lines))

        for result in results:
            client = result[result.index('boto3.client(\'') + 14: result.index('\')')]

            if client in PYTHON_EXCEPTIONS:
                client = PYTHON_EXCEPTIONS[client]

            clients.add('{}:*'.format(client))

        return list(clients)

    @staticmethod
    def is_handler_file(handler_lines):
        regex = re.compile(r'\s*def\s.*handler.*\(.*event, context\)')
        result = list(filter(regex.search, handler_lines))

        if result:
            return True, result[0]
        return False, None

    # could also check init file to make sure we are not retrieving a library
    @staticmethod
    def find_invoked_files(handler_file_lines):
        lines_without_comments = [x for x in handler_file_lines if not x.strip().startswith('#')]
        results = dict()

        from_regex_one = re.compile(r'from .*\..* import')
        from_regex_two = re.compile(r'from \w* import \w*')
        import_regex = re.compile(r'import .*\..*')

        for line in lines_without_comments:
            from_result_one = from_regex_one.search(line)
            from_result_two = from_regex_two.search(line)
            import_result = import_regex.search(line)

            if from_result_one:
                from_group = from_result_one.group(0)
                from_split = from_group.replace('from ', '').replace(' import', '').split('.')
                results[from_split[0]] = from_split[1]
            elif from_result_two:
                from_group = from_result_two.group(0)
                from_split = from_group.replace('from ', '').replace('import ', '').split(' ')
                results[from_split[0]] = from_split[1]
            elif import_result:
                import_group = import_result.group(0)
                import_split = import_group.replace('import ', '').split('.')
                results[import_split[0]] = import_split[1]

        return results

    @staticmethod
    def get_executable_glob():
        return '**/*.zip'

    def __repr__(self):
        return self.__class__.__name__
