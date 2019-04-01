def add_to_resources(lambdas):
    resources = {}

    for l in lambdas:
        if 'S3' in l['events']:
            resources['S3EventBucket'] = {
                'Type': 'AWS::S3::Bucket'
            }
        break

    return resources
