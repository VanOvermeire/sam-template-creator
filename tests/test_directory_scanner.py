import unittest

from read import directory_scanner


class TestDirectoryScanner(unittest.TestCase):
    def test_get_number_of_files_for_should_return_correct_number_of_files_for_suffix(self):
        result = directory_scanner.get_number_of_files_for('.py', ['some_file.py', 'secondfile.js', 'third_file.json', 'fourth.py'])

        self.assertEqual(result, 2)
