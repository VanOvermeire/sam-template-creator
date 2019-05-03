import os


class FileInfo:
    def __init__(self, location, directory, file, handler_line, lines, strategy, zip_file=None):
        self.location = str(location)
        self.directory = str(directory)
        self.file = str(file)
        self.handler_line = handler_line
        self.lines = lines
        self.strategy = strategy
        self.zip_file = zip_file

    def build_camel_case_name(self, dir_name):
        components = dir_name.split('_')

        return ''.join(x.title() for x in components)

    def build_uri(self, dir_name):
        if self.zip_file:
            return '{}/{}'.format(dir_name, self.zip_file)
        return '{}/'.format(dir_name)

    def build(self):
        dir_name = os.path.relpath(self.directory, self.location)
        name = self.build_camel_case_name(dir_name)
        uri = self.build_uri(dir_name)
        handler = self.strategy.build_handler(self.directory, self.file, self.handler_line)
        variables = self.strategy.find_env_variables(self.lines)
        permissions = self.strategy.find_role(self.lines)
        events = self.strategy.find_events(self.handler_line)
        api = self.strategy.find_api(self.handler_line)

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
        return '{}({}, {}, {}, {}, {}, {})'.format(self.__class__.__name__, self.location, self.directory, self.file, self.handler_line, self.lines, self.strategy)
