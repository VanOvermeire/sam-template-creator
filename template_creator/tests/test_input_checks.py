from pyfakefs.fake_filesystem_unittest import TestCase
from template_creator.util import input_checks


class TestInputChecks(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_check_runtime_fake_runtime_returns_false(self):
        result = input_checks.check_runtime('python1')

        self.assertFalse(result)

    # when all languages have been added, parameterized test to check all of them
    def test_check_runtime_python37_returns_true(self):
        result = input_checks.check_runtime('python3.7')

        self.assertTrue(result)

    def test_check_runtime_go1_returns_true(self):
        result = input_checks.check_runtime('go1.x')

        self.assertTrue(result)

    def test_check_location_with_directories_returns_true(self):
        self.fs.create_dir('/foo')
        self.fs.create_dir('/foo/bar')
        self.fs.create_dir('/foo/fiz')
        self.fs.create_file('/foo/somefile.py')

        result = input_checks.check_location('/foo')

        self.assertTrue(result)

    def test_check_location_without_directories_returns_false(self):
        self.fs.create_dir('/foo')
        self.fs.create_file('/foo/somefile.py')

        result = input_checks.check_location('/foo')

        self.assertFalse(result)

