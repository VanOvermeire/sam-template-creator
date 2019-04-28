def write_header():
    return {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Transform': 'AWS::Serverless-2016-10-31'
    }


def write_global_section(language, memory, timeout):
    return {
        'Globals': {
            'Function': {
                'Timeout': timeout,
                'Runtime': language,
                'MemorySize': memory
            }
        }
    }


def write_headers(config):
    headers = write_header()

    if not config['no-globals']:
        headers.update(write_global_section(config['language'], config['memory'], config['timeout']))

    return headers
