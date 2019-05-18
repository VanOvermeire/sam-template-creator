import sys
import argparse
import logging
from template_creator.util import input_checks

from template_creator import coordinator


def main():

    parser = argparse.ArgumentParser(description='Create a SAM template for your serverless project')
    parser.add_argument('-l', '--location', type=str, dest='location', required=True, help='absolute or relative location of your project')
    parser.add_argument('-lan', '--language', type=str, dest='language', required=False, help='set the language of your project (for example python3.7). If not set, the tool tries to guess the right language')
    parser.add_argument('-g', '--globals', dest='set_global', required=False, action='store_true', help='if used, the memory and timeout of the lambdas will be set globally instead of per function')
    parser.add_argument('-d', '--debug', dest='set_debug', required=False, action='store_true', help='set the logging level to debug')

    args = parser.parse_args()

    if args.set_debug:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    if not input_checks.config_checks(args.location, args.language):
        sys.exit(1)

    coordinator.find_resources_and_create_yaml_template(args.location, args.language, args.set_global)


if __name__ == "__main__":
    main()
