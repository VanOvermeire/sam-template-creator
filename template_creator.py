import coordinator
import argparse
from checks import checks

parser = argparse.ArgumentParser(description='Create a SAM template for your serverless project')
parser.add_argument('--location', type=str, dest='location', required=True, help='absolute location of your project')
parser.add_argument('--language', type=str, dest='language', required=False, help='set the language of your project (for example, . If not set, we will try to determine it ourselves.')

args = parser.parse_args()

if args.language is not None and not checks.check_runtime(args.language):
    exit(1)

coordinator.create_template(args.location)
