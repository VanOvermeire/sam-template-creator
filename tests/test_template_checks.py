import unittest

from util import template_checks


class TestInputChecks(unittest.TestCase):
    def test_build_backup_name(self):
        result = template_checks.build_backup_name('template.yaml')

        self.assertFalse('template.yaml' == result)
        self.assertTrue('template' in result)
        self.assertTrue('.yaml' in result)
