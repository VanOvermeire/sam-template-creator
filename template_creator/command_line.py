import argparse
from template_creator.util import input_checks

from template_creator import coordinator


def main():
    parser = argparse.ArgumentParser(description='Create a SAM template for your serverless project')
    parser.add_argument('--location', type=str, dest='location', required=True, help='absolute location of your project')
    parser.add_argument('--language', type=str, dest='language', required=False, help='set the language of your project (for example, . If not set, we will try to determine it.')
    parser.add_argument('--memory', type=str, dest='memory', required=False, help='set the memory of your lambdas( (globally). If not set, a default is chosen.')
    parser.add_argument('--timeout', type=str, dest='timeout', required=False, help='set the timeout of your lambdas( (globally). If not set, a default is chosen.')

    args = parser.parse_args()

    if not input_checks.config_checks(args.language, args.timeout, args.memory):
        exit(1)

    coordinator.find_resources_and_create_yaml_template(args.location, args.language, args.timeout, args.memory)


if __name__ == "__main__":
    main()
