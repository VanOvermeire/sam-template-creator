# SAM Template Creator

## Intro

![Alt Text](https://cl.ly/886452a42910/Screen%252520Recording%2525202019-04-01%252520at%25252006.43%252520PM.gif)

The SAM Template Creator helps you set up te Infrastructure as Code for an AWS serverless project. It reads your project folder and generates a SAM template from it, containing the necessary
functions, globals, environment variables, etc.

Compared to a full-fledged framework like Serverless, the scope of this template creator is very *limited*, offer far fewer features. 
On the other hand, it is very lightweight (only generating the SAM yaml file), simple to use (just run the script) and requires no config, though you 
do need to follow a few conventions to get the most out of it.

And for very complex use cases, only the original SAM and Cloudformation templates will suffice.

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
- if part of the name equals a http method, we assume you want to map it to an api gateway method with the path represented by the rest of the name. For example, if your handler function's name
is `def put_hello_world_hander(event, context)`, the function is mapped to a PUT to `/hello/world`.
- if the lambda is triggered by an event source, the name should reflect that. So if s3 is the source, the name of the event should contain `s3`, for example `s3event`. Similar for other event sources.
- we also assume that most of the 'setup' (creating clients and getting environment variables) will happen in the file containing the handler. This only temporary though. The plan is to scan other files and add their config as well.

##### Node

- TODO

##### Go

- TODO

### Project Structure

There are three main parts to this project
- read: contains files that help with reading the files in the project. The `FileInfo.py` class reads an individual file and retrieves
resources and other configuration information. Because files will look very different depending on the language, it uses the strategy pattern
to aid in these language-specific tasks. For example, when dealing with Python, the `PythonStrategy` class is used.
- middleware: these files and functions take the information from the read side and do transforms, adding/removing certain config, before this is
passed to the writers.
- write: these files are responsible for writing the information to yaml.

Finally, there is a checks directory for checks on input, `coordinator.py`, which coordinates the work of the other files and `template_creator.py`,
which contains the argument parser and calls the coordinator.

### TODO Priorities

+++ Setup an integration test  
+++ Add other languages, via strategy
+++ For an S3 event, a bucket in the same template is required -> same for other kinds of events? If so, add logic for that 

++ Improvements in versatility. For example safer extraction of variables/events/...
++ Ask questions! See you call dynamo, add to template? generate outputs? how many buckets for events? deploy template? -> probably first read and then ask questions before passing info to writer  
++ Installer  
++ Generate requirements.txt

+ relative location of project  
+ git hook that creates new exe before pushing to remote
+ Option to specify folders to look for in project
+ Config option: set memory/timeout on individual lambdas vs globally
