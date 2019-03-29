import coordinator
import argparse

parser = argparse.ArgumentParser(description='Create a SAM template for your serverless project')
parser.add_argument('--location', type=str, dest='location', help='absolute location of your project')

args = parser.parse_args()
print(args.location)

