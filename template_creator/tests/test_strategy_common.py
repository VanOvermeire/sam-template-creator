import unittest

from template_creator.reader import language_strategy_common


class TestCommonStrategy(unittest.TestCase):

    def test_find_events(self):
        result = language_strategy_common.find_events('s3event')

        self.assertEqual(result, ['S3'])

    def test_find_events_with_underscore_in_name_event(self):
        result = language_strategy_common.find_events('sqs_event')

        self.assertEqual(result, ['SQS'])

    def test_find_events_no_events(self):
        result = language_strategy_common.find_events('an_event')

        self.assertIsNone(result)

    def test_find_cloudwatch_event(self):
        result = language_strategy_common.find_events('cloudwatch_event')

        self.assertEqual(result, ['CloudwatchEvent'])

    def test_find_cloudwatch_log_event(self):
        result = language_strategy_common.find_events('cloudwatch_logs_event')

        self.assertEqual(result, ['CloudWatchLogs'])
