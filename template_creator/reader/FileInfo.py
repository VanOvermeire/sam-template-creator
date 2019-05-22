import os


class FileInfo:
    def __init__(self, location, directory, file, handler_line, handler_lines, strategy, other_file_lines, executable=None):
        self.location = str(location)
        self.directory = str(directory)
        self.file = str(file)
        self.handler_line = handler_line
        self.handler_file_lines = handler_lines
        self.strategy = strategy
        self.other_file_lines = other_file_lines
        self.executable = executable

    def build_uri(self, dir_name):
        if self.executable:
            return os.path.relpath(self.executable, self.location)
        return '{}/'.format(dir_name)

    def build(self):
        dir_name = os.path.relpath(self.directory, self.location)
        # TODO camel case not suited for dots (java) or camelcase dirs
        name = self.strategy.build_camel_case_name(dir_name, self.file)
        uri = self.build_uri(dir_name)
        handler = self.strategy.build_handler(self.directory, self.file, self.handler_line, self.executable)
        events = self.strategy.find_events(self.handler_line)
        api = self.strategy.find_api(self.handler_line)
        all_file_lines = self.handler_file_lines + self.other_file_lines
        variables = self.strategy.find_env_variables(all_file_lines)
        permissions = self.strategy.find_permissions(all_file_lines)

        return {
            'name': name,
            'handler': handler,
            'uri': uri,
            'variables': variables,
            'events': events,
            'permissions': permissions,
            'api': api
        }

    def __repr__(self):
        return '{}({}, {}, {}, {}, {}, {})'.format(self.__class__.__name__, self.location, self.directory, self.file, self.handler_line, self.handler_file_lines, self.strategy)
