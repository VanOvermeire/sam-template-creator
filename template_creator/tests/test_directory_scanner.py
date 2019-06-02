from pathlib import Path
from pyfakefs.fake_filesystem_unittest import TestCase

from template_creator.reader import directory_scanner
from template_creator.reader.strategies.GoStrategy import GoStrategy
from template_creator.reader.strategies.PythonStrategy import PythonStrategy


class TestDirectoryScanner(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_get_number_of_files_for_should_return_correct_number_of_files_for_suffix(self):
        result = directory_scanner.get_number_of_files_for('.py', ['some_file.py', 'secondfile.js', 'third_file.json', 'fourth.py'])

        self.assertEqual(result, 2)

    def test_find_all_non_hidden_files_and_dirs_should_return_everything_except_hidden_files(self):
        self.fs.create_dir('/foo')
        self.fs.create_dir('/foo/bar')
        self.fs.create_dir('/foo/.idea')
        self.fs.create_file('/foo/somefile.py')
        self.fs.create_file('/foo/.hidden_file')

        results = directory_scanner.find_all_non_hidden_files_and_dirs('/foo')

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].name, 'bar')
        self.assertEqual(results[1].name, 'somefile.py')

    def test_guess_language_should_return_language_with_most_files(self):
        self.fs.create_dir('/root')
        self.fs.create_dir('/root/subdir_one')
        self.fs.create_file('/root/subdir_one/first_python.py')
        self.fs.create_file('/root/subdir_one/second_python.py')
        self.fs.create_dir('/root/subdir_two')
        self.fs.create_file('/root/subdir_two/first_go.go')
        self.fs.create_file('/root/subdir_two/second_go.go')
        self.fs.create_dir('/root/third_go.go')
        self.fs.create_file('/root/atextfile.txt')

        result = directory_scanner.guess_language('/root')

        self.assertEqual(result, 'go1.x')

    def test_executables_in_dir_should_find_executable_for_go(self):
        self.fs.create_dir('/root')
        self.fs.create_dir('/root/subdir_one')
        self.fs.create_file('/root/subdir_one/first_python.py')
        self.fs.create_file('/root/subdir_one/second_python.py')
        self.fs.create_dir('/root/subdir_two')
        self.fs.create_file('/root/subdir_two/first_go.go')
        self.fs.create_file('/root/subdir_two/second_go.go')
        self.fs.create_file('/root/subdir_two/main')
        self.fs.create_dir('/root/third_go.go')
        self.fs.create_file('/root/atextfile.txt')

        result = directory_scanner.executables_in_dir(Path('/root/subdir_two'), GoStrategy())

        self.assertEqual(result, '/root/subdir_two/main')

    def test_executables_in_dir_should_find_nested_executable_for_go(self):
        self.fs.create_dir('/root')
        self.fs.create_dir('/root/subdir_one')
        self.fs.create_file('/root/subdir_one/first_python.py')
        self.fs.create_file('/root/subdir_one/second_python.py')
        self.fs.create_dir('/root/subdir_two')
        self.fs.create_file('/root/subdir_two/first_go.go')
        self.fs.create_file('/root/subdir_two/second_go.go')
        self.fs.create_file('/root/subdir_two/dist/main')
        self.fs.create_dir('/root/third_go.go')
        self.fs.create_file('/root/atextfile.txt')

        result = directory_scanner.executables_in_dir(Path('/root/subdir_two'), GoStrategy())

        self.assertEqual(result, '/root/subdir_two/dist/main')

    def test_executables_in_dir_should_find_executable_for_python(self):
        self.fs.create_dir('/root')
        self.fs.create_dir('/root/subdir_one')
        self.fs.create_file('/root/subdir_one/first_python.py')
        self.fs.create_file('/root/subdir_one/second_python.py')
        self.fs.create_file('/root/subdir_one/wrapped_code.zip')
        self.fs.create_dir('/root/subdir_two')
        self.fs.create_file('/root/subdir_two/first_go.go')
        self.fs.create_file('/root/subdir_two/second_go.go')
        self.fs.create_dir('/root/third_go.go')
        self.fs.create_file('/root/atextfile.txt')

        result = directory_scanner.executables_in_dir(Path('/root/subdir_one'), PythonStrategy())

        self.assertEqual(result, '/root/subdir_one/wrapped_code.zip')

    def test_executables_in_dir_should_find_nested_executable_for_python(self):
        self.fs.create_dir('/root')
        self.fs.create_dir('/root/subdir_one')
        self.fs.create_file('/root/subdir_one/first_python.py')
        self.fs.create_file('/root/subdir_one/second_python.py')
        self.fs.create_file('/root/subdir_one/dist/wrapped_code.zip')
        self.fs.create_dir('/root/subdir_two')
        self.fs.create_file('/root/subdir_two/first_go.go')
        self.fs.create_file('/root/subdir_two/second_go.go')
        self.fs.create_dir('/root/third_go.go')
        self.fs.create_file('/root/atextfile.txt')

        result = directory_scanner.executables_in_dir(Path('/root/subdir_one'), PythonStrategy())

        self.assertEqual(result, '/root/subdir_one/dist/wrapped_code.zip')

    def test_executables_in_dir_should_ignore_multiple_executables_for_go(self):
        self.fs.create_dir('/root')
        self.fs.create_dir('/root/subdir_one')
        self.fs.create_file('/root/subdir_one/first_python.py')
        self.fs.create_file('/root/subdir_one/second_python.py')
        self.fs.create_dir('/root/subdir_two')
        self.fs.create_file('/root/subdir_two/first_go.go')
        self.fs.create_file('/root/subdir_two/second_go.go')
        self.fs.create_file('/root/subdir_two/main')
        self.fs.create_file('/root/subdir_two/dist/main')
        self.fs.create_dir('/root/third_go.go')
        self.fs.create_file('/root/atextfile.txt')

        result = directory_scanner.executables_in_dir(Path('/root/subdir_two'), GoStrategy())

        self.assertIsNone(result)

    def test_executables_in_dir_should_ignore_multiple_executables_for_python(self):
        self.fs.create_dir('/root')
        self.fs.create_dir('/root/subdir_one')
        self.fs.create_file('/root/subdir_one/first_python.py')
        self.fs.create_file('/root/subdir_one/second_python.py')
        self.fs.create_file('/root/subdir_one/dist/wrapped_code.zip')
        self.fs.create_file('/root/subdir_one/wrapped_code.zip')
        self.fs.create_dir('/root/subdir_two')
        self.fs.create_file('/root/subdir_two/first_go.go')
        self.fs.create_file('/root/subdir_two/second_go.go')
        self.fs.create_dir('/root/third_go.go')
        self.fs.create_file('/root/atextfile.txt')

        result = directory_scanner.executables_in_dir(Path('/root/subdir_two'), PythonStrategy())

        self.assertIsNone(result)

    def test_check_language_file_for_lambda_should_return_false_if_no_handler(self):
        self.fs.create_dir('/root')
        self.fs.create_dir('/root/subdir_one')
        self.fs.create_file('/root/subdir_one/first_python.py', contents='some content here')
        self.fs.create_file('/root/subdir_one/second_python.py')
        self.fs.create_file('/root/subdir_one/dist/wrapped_code.zip')
        self.fs.create_file('/root/subdir_one/wrapped_code.zip')
        self.fs.create_dir('/root/subdir_two')
        self.fs.create_file('/root/subdir_two/first_go.go')
        self.fs.create_file('/root/subdir_two/second_go.go')
        self.fs.create_dir('/root/third_go.go')
        self.fs.create_file('/root/atextfile.txt')

        found, result = directory_scanner.check_language_file_for_lambda(Path('/root/subdir_one/first_python.py'), Path('/root/subdir_one'),
                                                                         [Path('/root/subdir_one'), Path('/root/subdir_two')], '/root', 'python3.7')

        self.assertFalse(found)
        self.assertIsNone(result)

    def test_check_language_file_for_lambda_should_return_true_and_file_info_if_handler(self):
        self.fs.create_dir('/root')
        self.fs.create_dir('/root/subdir_one')
        self.fs.create_file('/root/subdir_one/first_python_a_handler.py', contents='def lambda_handler(s3event, context):\n')
        self.fs.create_file('/root/subdir_one/second_python.py')
        self.fs.create_dir('/root/subdir_two')
        self.fs.create_file('/root/subdir_two/first_go.go')
        self.fs.create_file('/root/subdir_two/second_go.go')
        self.fs.create_dir('/root/third_go.go')
        self.fs.create_file('/root/atextfile.txt')

        found, result = directory_scanner.check_language_file_for_lambda(Path('/root/subdir_one/first_python_a_handler.py'), Path('/root/subdir_one'),
                                                                         [Path('/root/subdir_one'), Path('/root/subdir_two')], '/root', 'python3.7')

        self.assertTrue(found)
        self.assertEqual(result['name'], 'SubdirOne')
        self.assertEqual(result['handler'], 'first_python_a_handler.lambda_handler')
        self.assertEqual(result['uri'], 'subdir_one/')

    def test_find_lambdas_should_find_all_lambdas(self):
        self.fs.create_dir('/root')
        self.fs.create_dir('/root/subdir_one')
        self.fs.create_file('/root/subdir_one/first_python_a_handler.py', contents='def lambda_handler(s3event, context):\n')
        self.fs.create_file('/root/subdir_one/second_python.py')
        self.fs.create_dir('/root/subdir_two')
        self.fs.create_file('/root/subdir_two/third_python.py', contents='def lambda_handler(an_event, context):\n')
        self.fs.create_dir('/root/third_go.go')
        self.fs.create_file('/root/atextfile.txt')

        result = directory_scanner.find_lambda_files_in_directory('/root', 'python3.7')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'SubdirOne')
        self.assertEqual(result[1]['name'], 'SubdirTwo')
