import unittest

import coordinator


# TODO additional tests, maybe with mocking of our own classes
class TestCoordinator(unittest.TestCase):
    def test_full_location_template_without_ending_forward_slash(self):
        result = coordinator.full_location_template('/some/location', 'template.yaml')

        self.assertEqual(result, '/some/location/template.yaml')

    def test_full_location_template_with_ending_forward_slash(self):
        result = coordinator.full_location_template('/some/location/', 'template.yaml')

        self.assertEqual(result, '/some/location/template.yaml')
