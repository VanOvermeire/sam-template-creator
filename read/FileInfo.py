import os

# this class will also need a strategy to do some stuff - for example, for build_handler (now specifically python)
import re


class FileInfo:
    def __init__(self, location, directory, file, handler_line, lines):
        self.location = str(location)
        self.directory = str(directory)
        self.file = str(file)
        self.handler_line = handler_line
        self.lines = lines

    def build_handler(self):
        file_name = os.path.relpath(self.file, self.directory)
        function_name = self.handler_line[self.handler_line.index('def') + 4:self.handler_line.index('(')]
        file_name = file_name[0:file_name.index('.')]

        return '{}.{}'.format(file_name, function_name)

    def build_camel_case_name(self, dir_name):
        components = dir_name.split('_')

        return ''.join(x.title() for x in components)

    def find_env_variables(self):
        variables = []
        first_regex = re.compile(r'.*os.environ\[.*')
        second_regex = re.compile(r'.*os.environ.get\(.*')
        first_regex_results = list(filter(first_regex.search, self.lines))
        second_regex_results = list(filter(second_regex.search, self.lines))
        # BUCKET = os.environ.get('BUCKET')

        # TODO too simple, might not work in more complex situations
        for result in first_regex_results:
            variable = result[result.index('os.environ[\'') + 12: result.index('\']')]
            variables.append(variable)

        for result in second_regex_results:
            variable = result[result.index('os.environ.get(\'') + 16: result.index('\')')]
            variables.append(variable)

        return variables

    def build(self):
        dir_name = os.path.relpath(self.directory, self.location)
        handler = self.build_handler()
        variables = self.find_env_variables()

        return {'name': self.build_camel_case_name(dir_name), 'handler': handler, 'uri': '{}/'.format(dir_name), 'variables': variables}
