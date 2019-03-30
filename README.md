# AWS Serverless Template Creator

## Intro

The AWS Serverless Template Creator helps you set up te Infrastructure as Code for an AWS serverless project. 

It produces a template.yaml file, containing a SAM template, which you can then deploy to AWS, using 

`aws cloudformation package --template-file template.yaml --s3-bucket A-BUCKET-NAME --output-template-file outputSamTemplate.yaml`

## Requirements

- python 3
- a project directory to scan 

Right now only python projects are supported.

## Usage

Run the `create_executable.sh` or clone this project and run `python template_creator.py`. 

This will create a `template.yaml` file in the root of your project's directory. Check its contents! It might point out some things you have to fill in. 

### Notes

*Warning!* Serverless Template Creator requires your project to be organised in a certain way. 

Take note of the following:

#### Directory

Every lambda should have its own directory, under the root of the project. Other files can be present in the same directory.

#### Naming conventions

Python:
- the name of the Lambda handler function should contain the word 'handler'. The event should end with 'event' and the context should be named 'context'. For instance `def lambda_handler(s3event, context):`
- if the lambda is triggered by an event source, the name should reflect that. So if s3 is the source, the name of the event should contain `s3`, for example `s3event`. Similar for other event sources.

Node:
- ...

Go:
- ...

### TODO

Overall
- Add other languages, via strategy
- Add gif demonstrating capabilities
- Option to specify folders to look for in project
- Config option: set memory/timeout on individual lambdas vs globally
- Ask questions: see you call dynamo, add to template? generate outputs? deploy template?

Improvements
- Api? Similar to events
- Generate requirements.txt? -> or does SAM package get the right dependencies?
- Setup an integration test! (And add more tests)
