import os


# this class will also need a strategy to do some stuff - for example, for build_handler (now specifically python)
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

    def build(self):
        dir_name = os.path.relpath(self.directory, self.location)
        handler = self.build_handler()

        return {'name': self.build_camel_case_name(dir_name), 'handler': handler, 'uri': '{}/'.format(dir_name)}
