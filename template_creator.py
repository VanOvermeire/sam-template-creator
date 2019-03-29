import coordinator
import argparse

parser = argparse.ArgumentParser(description='Create a SAM template for your serverless project')
parser.add_argument('--location', type=str, dest='location', required=True, help='absolute location of your project')

args = parser.parse_args()

coordinator.create_template(args.location)
