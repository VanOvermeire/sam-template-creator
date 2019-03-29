import directory_scanner
import yaml_writer

# TODO make stuff configurable: overwrite locations to check (ignore some?), language, mem size, etc.

location = '/Users/samvanovermeire/Documents/transcription-backend/'

language, suffix = directory_scanner.guess_language(location)
lambdas = directory_scanner.find_directory(location, suffix)

yaml_writer.write({'language': language, 'lambdas': lambdas})

