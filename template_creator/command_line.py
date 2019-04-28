import argparse
from template_creator.util import input_checks

from template_creator import coordinator


def main():
    parser = argparse.ArgumentParser(description='Create a SAM template for your serverless project')
    parser.add_argument('-l', '--location', type=str, dest='location', required=True, help='absolute location of your project')
    parser.add_argument('-lan', '--language', type=str, dest='language', required=False, help='set the language of your project (for example, . If not set, we will try to determine it.')
    parser.add_argument('-mem', '--memory', type=str, dest='memory', required=False, help='set the memory of your lambdas( (globally). If not set, a default is chosen.')
    parser.add_argument('-tim', '--timeout', type=str, dest='timeout', required=False, help='set the timeout of your lambdas( (globally). If not set, a default is chosen.')
    parser.add_argument('-ng', '--no-globals', dest='no_globals', required=False, action='store_true', help='if used, globals will not be used and memory, timeout and size will be set per function')

    args = parser.parse_args()

    if not input_checks.config_checks(args.language, args.timeout, args.memory):
        exit(1)

    coordinator.find_resources_and_create_yaml_template(args.location, args.language, args.timeout, args.memory, args.no_globals)


if __name__ == "__main__":
    main()
