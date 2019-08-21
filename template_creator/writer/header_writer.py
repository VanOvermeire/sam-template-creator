def _write_root_level_header():
    return {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Transform': 'AWS::Serverless-2016-10-31'
    }


def _write_global_section(language):
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
    headers = _write_root_level_header()

    if config['set-global']:
        headers.update(_write_global_section(config['language']))

    return headers
