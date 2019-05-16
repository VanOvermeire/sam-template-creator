def create_additional_resources(lambdas):
    resources = {}

    for l in lambdas:
        if l['events'] and 'S3' in l['events']:
            # TODO what if there are multiple event buckets?
            add_required_s3_bucket(resources)
            break

    return resources


def add_required_s3_bucket(resources):
    resources['S3EventBucket'] = {
        'Type': 'AWS::S3::Bucket'
    }
