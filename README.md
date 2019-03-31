# SAM Template Creator

## Intro

The SAM Template Creator helps you set up te Infrastructure as Code for an AWS serverless project. It reads your project folder and generates a SAM template from it, containing the necessary
functions, globals, environment variables, etc.

## Requirements

- python 3
- a project directory to scan 

*For the moment only python 3 projects are supported. Node, Go and Java are planned.*

## Usage

Run the `create_executable.sh` or clone this project and run `python template_creator.py --location /absolute/path/to/location`. 

Additional (optional) arguments are:
- language: can be useful if you think the script will not be able to guess the language (it checks the number of files per language and takes the highest), or if you want to get an older version
of a runtime (because left by itself, the script will default to the latest version of, for example, python)
- memory: memory you want to set for your lambdas. Defaults to 512
- timeout: the timeout for your lambdas. Defaults to 3

The script will create a `template.yaml` file in the root of your project's directory. Check its contents! It might point out some things you have to fill in.

You can then deploy the template to AWS, using 

`aws cloudformation package --template-file template.yaml --s3-bucket YOUR-BUCKET-NAME --output-template-file outputSamTemplate.yaml --capabilities CAPABILITY_IAM`

### Notes on usage

*Be aware:* SAM Template Creator requires your project to be organised in a certain way.

#### Directory

Every lambda should have its own directory, under the root of the project. Other files can be present in the same directory.

#### Naming conventions

##### Python

- the name of the Lambda handler function should contain the word 'handler'. The event should end with 'event' and the context should be named 'context'. For instance `def lambda_handler(s3event, context):`
- if the lambda is triggered by an event source, the name should reflect that. So if s3 is the source, the name of the event should contain `s3`, for example `s3event`. Similar for other event sources.
- we also assume that most of the 'setup' (creating clients and getting environment variables) will happen in the file containing the handler. In the future, we may change this and scan other files for setup as well.

##### Node
- TODO

### TODO

+++ Api? Similar to events  
+++ Generate requirements.txt? -> or does SAM package get the right dependencies?  
+++ Setup an integration test  
+++ Add other languages, via strategy  
+++ better extraction of variables/events/... 
+++ For an S3 event, a bucket in the same template is required -> same for other kinds of events? If so, add logic for that 

++ Ask questions! See you call dynamo, add to template? generate outputs? how many buckets for events? deploy template? -> probably first read and then ask questions before passing info to writer  
++ Installer  
++ Complete readme  
++ Output some additional guidance, depending on what was added (events, env vars, etc.) -> or ask questions about them  
++ relative location of project  

+ Add gif demonstrating capabilities
+ git hook that creates new exe before pushing to remote
+ Option to specify folders to look for in project
+ Config option: set memory/timeout on individual lambdas vs globally
