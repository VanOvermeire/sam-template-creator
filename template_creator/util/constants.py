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

HTTP_METHODS = ['get', 'head', 'options', 'post', 'put', 'delete', 'any']

# list of our event types
# api is handled separately, logic for cloudwatch logs and events is a bit special
EVENT_TYPES = {
    'S3': {
        'Type': 'S3',
        'Properties': {
            'Bucket': {
                'Ref': 'S3EventBucket'
            },
            'Events': 's3:ObjectCreated:*'
        }
    },
    'SNS': {
        'Type': 'SNS',
        'Properties': {
            'Topic': 'ARN-OF-YOUR-TOPIC'
        }
    },
    'Kinesis': {
        'Type': 'Kinesis',
        'Properties': {
            'Stream': 'ARN-OF-YOUR-STREAM',
            'StartingPosition': 'TRIM_HORIZON',
            'BatchSize': 10,
            'Enabled': True
        }
    },
    'DynamoDB': {
        'Type': 'DynamoDB',
        'Properties': {
            'Stream': 'ARN-OF-YOUR-STREAM',
            'StartingPosition': 'TRIM_HORIZON',
            'BatchSize': 10,
            'Enabled': True
        }
    },
    'SQS': {
        'Type': 'SQS',
        'Properties': {
            'Queue': 'ARN-OF-YOUR-QUEUE',
            'BatchSize': 10,
            'Enabled': True
        }
    },
    'IoTRule': {
        'Type': 'IoTRule',
        'Properties': {
            'Sql': '"SELECT * FROM example"'
        }
    },
    'Schedule': {
        'Type': 'Schedule',
        'Properties': {
            'Schedule': 'rate(5 minutes) # OR cron(5 * * * ? *)'
        }
    },
    'CloudWatchLogs': {
        'Type': 'CloudWatchLogs',
        'Properties': {
            'LogGroupName': 'NAME-OF-CLOUDWATCH-LOG-GROUP',
            'FilterPattern': 'Error'
        }
    },
    'CloudwatchEvent': {
        'Type': 'CloudWatchEvent',
        'Properties': {
            'Pattern': {
                'detail': {
                    'key': 'value'
                }
            }
        }
    }
}
