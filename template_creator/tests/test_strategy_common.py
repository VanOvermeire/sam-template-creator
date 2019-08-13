import unittest

from template_creator.reader.strategies import language_strategy_common


class TestCommonStrategy(unittest.TestCase):

    def test_find_events_no_events(self):
        result = language_strategy_common.find_events('an_event')

        self.assertIsNone(result)

    def test_find_events(self):
        result = language_strategy_common.find_events('s3event')

        self.assertEqual(result, ['S3'])

    def test_find_sqs_event_with_underscore_in_name_event(self):
        result = language_strategy_common.find_events('sqs_event')

        self.assertEqual(result, ['SQS'])

    def test_find_dynamodb_event_with_underscore_in_name_event(self):
        result = language_strategy_common.find_events('dynamodb_event')

        self.assertEqual(result, ['DynamoDB'])

    def test_find_sns_event_without_underscore_in_name_event(self):
        result = language_strategy_common.find_events('snsevent')

        self.assertEqual(result, ['SNS'])

    def test_find_cloudwatch_event(self):
        result = language_strategy_common.find_events('cloudwatch_event')

        self.assertEqual(result, ['CloudwatchEvent'])

    def test_find_cloudwatch_log_event(self):
        result = language_strategy_common.find_events('cloudwatch_logs_event')

        self.assertEqual(result, ['CloudWatchLogs'])

    def test_find_schedule_event(self):
        result = language_strategy_common.find_events('schedule_event')

        self.assertEqual(result, ['Schedule'])

    def test_find_schedule_event_with_specified_rate(self):
        result = language_strategy_common.find_events('every_3_hours_event')

        self.assertEqual(result, ['Schedule:3 hours'])
