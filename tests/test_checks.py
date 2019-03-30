import unittest

from checks import checks


class TestChecks(unittest.TestCase):
    def test_check_runtime_fake_runtime_returns_false(self):
        result = checks.check_runtime('python1')

        self.assertFalse(result)

    # when all languages have been added, parameterized test to check all of them
    def test_check_runtime_real_runtime_returns_true(self):
        result = checks.check_runtime('python3.7')

        self.assertFalse(result)

    def test_build_backup_name(self):
        result = checks.build_backup_name('template.yaml')

        self.assertFalse('template.yaml' == result)
        self.assertTrue('template' in result)
        self.assertTrue('.yaml' in result)
