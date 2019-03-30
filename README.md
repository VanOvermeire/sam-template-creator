# AWS Serverless Template Creator

## Requirements

- python 3
- a project directory to scan (right now only python projects are supported)

## Usage

Run the `create_executable.sh` or clone this project and run `python template_creator.py`. 

This will create a `template.yaml` file in the root of your project's directory. Check its contents, it might point out some things you have to fill in. 

### TODO

Overall
- Use strategy to analyze files per language

Improvements
- Try to find right roles, from templates of SAM
- Right events? - may need some additional info for that...
- Similar for api
- Generate requirements.txt? -> or does SAM package get the right dependencies?
- Config option: set memory/timeout on individual lambdas vs globally

Cleanup
- Remove temp
