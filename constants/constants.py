LANGUAGES_WITH_SUFFIXES = {
    'python3.7': '.py',
    'python3.6': '.py',
    'python2.7': '.py',
    'nodejs8.10': '.js',
    'nodejs6.10': '.js',
    'nodejs4.3': '.js',
    'java8': '.java',
    'go1.x': '.go'
}


# TODO add other event types (and check whether they work with underscores, for example sns_event)
EVENT_TYPES = {
    'S3': {
        'Type': 'S3',
        'Properties': {
            'Bucket': 'Fill in value and change event - object created - if needed',
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
