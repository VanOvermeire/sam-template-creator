def write_header():
    return {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Transform': 'AWS::Serverless-2016-10-31'
    }


def write_global_section(language):
    return {
        'Globals': {
            'Function': {
                'Runtime': language,
                'Timeout': 3,
                'MemorySize': 512
            }
        }
    }


def write_headers(config):
    headers = write_header()

    if config['set-global']:
        headers.update(write_global_section(config['language']))

    return headers
