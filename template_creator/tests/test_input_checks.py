import unittest

from template_creator.util import input_checks


class TestInputChecks(unittest.TestCase):
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
