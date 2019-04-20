import unittest

from template_creator.util import input_checks


class TestInputChecks(unittest.TestCase):
    def test_check_runtime_fake_runtime_returns_false(self):
        result = input_checks.check_runtime('python1')

        self.assertFalse(result)

    # when all languages have been added, parameterized test to check all of them
    def test_check_runtime_real_runtime_returns_true(self):
        result = input_checks.check_runtime('python3.7')

        self.assertTrue(result)

    def test_check_timeout_valid_timeout_returns_true(self):
        result = input_checks.check_timeout(15)

        self.assertTrue(result)

    def test_check_timeout_invalid_timeout_returns_false(self):
        result = input_checks.check_timeout(1001)

        self.assertFalse(result)

    def test_check_timeout_not_a_number_returns_false(self):
        result = input_checks.check_timeout('fake')

        self.assertFalse(result)

    def test_check_memory_valid_memory_returns_true(self):
        result = input_checks.check_memory(256)

        self.assertTrue(result)

    def test_check_memory_invalid_memory_returns_false(self):
        result = input_checks.check_memory(4000)

        self.assertFalse(result)

    def test_check_memory_not_a_number_memory_returns_false(self):
        result = input_checks.check_memory('fake')

        self.assertFalse(result)

    def test_check_memory_not_divisible_by_two_returns_false(self):
        result = input_checks.check_memory(255)

        self.assertFalse(result)

    def test_config_checks_valid_returns_true(self):
        result = input_checks.config_checks('python3.7', 30, 512)

        self.assertTrue(result)

    def test_config_checks_invalid_returns_false(self):
        result = input_checks.config_checks('python3.7', 30, 6000)

        self.assertFalse(result)


