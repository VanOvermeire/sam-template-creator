import unittest

from read import strategy_builder
from read.PythonStrategy import PythonStrategy


class TestStrategyBuilde(unittest.TestCase):
    def test_build_strategy_returns_correct_strategy_for_language(self):
        result = strategy_builder.build_strategy('python3.7')

        self.assertTrue(isinstance(result, PythonStrategy))

    def test_build_strategy_throws_exception_for_unknown_language(self):
        with self.assertRaises(Exception):
            strategy_builder.build_strategy('fake')
