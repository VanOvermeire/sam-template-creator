# AWS Serverless Template Creator

## Requirements

- python 3
- a project directory to scan (right now only python projects are supported)

## Usage

Run the `create_executable.sh` or clone this project and run `python template_creator.py`

### TODO

- Use strategy to analyze files per language
- Try to find right roles, from templates of SAM
- Right events?
- Generate requirements.txt? -> or does SAM package get the right dependencies?
- Run SAM package as a check
- More config options: language, location, memory size, timeout, etc.
- Tests...
- Remove temp
