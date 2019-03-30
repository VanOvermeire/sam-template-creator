# TODO add other runtimes, add other event types (and check whether they work with underscores, for example sns_event)

LANGUAGES_WITH_SUFFIXES = {
    'python3.7': '.py',
    'nodejs8.10': '.js'
}

EVENT_TYPES = {
    'S3': {
        'Type': 'S3',
        'Properties': {
            'Bucket': 'FILL IN VALUE (and change event if needed)',
            'Events': 's3:ObjectCreated:*'
        }
    },
    'SNS': {},
    'Kinesis': {},
    'DynamoDB': {},
    'SQS': {},
    'Api': {},
    'Schedule': {},
    'CloudWatchEvent': {},
    'CloudWatchLogs': {},
    'IoTRule': {},
    'AlexaSkill': {}
}
