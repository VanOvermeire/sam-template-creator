# SAM Template Creator

## Intro

![Alt Text](https://cl.ly/21b792e2627b/Screen%252520Recording%2525202019-04-21%252520at%25252010.56%252520AM.gif)

The SAM Template Creator helps you set up Infrastructure as Code for an AWS serverless project.
It reads your project folder and generates a [SAM template][1] containing the necessary functions, globals, environment variables, etc.

Compared to a full-fledged framework like [Serverless][2], the scope of this template creator is *limited*. But this has advantages as well:
the tool is lightweight, generating no additional files except your IaC yaml, and is simple to use.

Finally, the tool will probably be insufficient to handle very complex use-cases, though it can still provide a starting point to expand upon.

[1]: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md
[2]: https://serverless.com/

## Requirements

- python 3.5 or higher
- pip
- a serverless project to scan. *Currently only Python and Go projects are supported. Node and Java are planned.*

## Usage Guide / How-to

Install the tool using pip

```
pip install sam-template-creator

# or alternatively

pip3 install sam-template-creator
```

Now either go to the root directory of your project and type

```
sam-template-creator --location .

# or with shorthand argument names

sam-template-creator -l .
```

The tool will also work with absolute paths 

`sam-template-creator --location /path/to/project`

The script will create a `template.yaml` file in the root of your project's directory. Check its contents! It might point out some things you have to fill in.

You can also pass some (optional) arguments:

- language: by default, the tool will guess which language the project is written in. If it does not find the correct language, or if you want an older version of
the runtime (the script will default to the latest version), you can use this argument.
- globals: if used, the memory and timeout of the lambdas will be set globally, instead of per function

With your template created, you should now be able to deploy to AWS using

```
aws cloudformation package --template-file template.yaml --s3-bucket YOUR-BUCKET-NAME --output-template-file outputSamTemplate.yaml
aws cloudformation deploy --template-file outputSamTemplate.yaml --stack-name PICK-A-STACK-NAME --capabilities CAPABILITY_IAM
```

### Notes on usage

*Important!* SAM Template Creator requires your project to be organised in a certain way.

See generics (across languages) and specifics (per language) below.

#### Directory

Every lambda should have its own directory, under the root of the project. Other files can be present in the same directory.
The tool will scan both the file containing the handler and files it directly refers to for information on required permissions, environment variables, etc. 

If a single zip (for most languages) or executable is present in the folder of the handler file, or a subfolder, 
the tool assumes this zip contains the code you want to upload to AWS.

#### Naming conventions

##### Python

- the name of the Lambda handler function should contain the word 'handler'. The event should end with 'event' and the context should be 'context'. 
For example `def lambda_handler(s3event, context)`
- if part of the name equals a http method, we assume you want to map it to an api gateway method with the path represented by the rest of the name. 
For example, if your handler's name is `def put_hello_world_hander(event, context)`, the function is mapped to a `PUT` to `/hello/world`.
- if the lambda is triggered by an event source, the name should reflect this. 
For example, if s3 is the source, the name of the event should contain `s3`: `s3event` or `s3_event` or...

##### Go

- the name of your executable should be `handler`, except if you have an executable in the folder of your lambda. If so, the tool will assume that this
executable has the code of your lambda. It will set `Handler` and `CodeUri` accordingly.  
For example, if your folder `mylambda` contains a `main` file under `dist/main`, the `Handler` will become `main`, with the `CodeUri` equal to `/mylambda/dist/main`. 
- if you want to map a function to an api gateway method, the lambda handler should end with the word Request, with the path and method prepended to this word.
For example, `func PostAddHelloRequest(_ context.Context, event events.APIGatewayProxyRequest) error` is mapped to a `POST` to `/add/hello`.
- if the lambda is triggered by an event source, the name should reflect that. 
For example, if s3 is the source, the name of the event should contain `s3`, like this: `s3event` or `s3_event` or...

##### Node

- TODO

##### Java

- TODO

### Project Structure

There are three main parts to this project
- `reader`: contains files that help with reading the files in the project. The `FileInfo.py` class reads an individual file and retrieves
resources and other configuration information. Because files will look very different depending on the language, it uses the strategy pattern
to aid in these language-specific tasks. For example, when dealing with Python, the `PythonStrategy` class is used.
- `middleware`: these files and functions take the information from the read side and do transforms, adding/removing certain config, before this is
passed to the writers.
- `writer`: these files are responsible for writing the information to yaml.

Besides these folders, there is a `util` folder, the `coordinator.py` file which coordinates the work of the other files and the `command_line.py`,
which contains the argument parser and calls the coordinator after checking the input.

### Tests

Unit tests can be run with `python -m unittest`. A relatively simple it-test is run with the bash script `test.sh` under tests/it-test.
It requires a bucket as argument (for uploading the lambda zip) and [default AWS credentials][3].

[3]: https://docs.aws.amazon.com/polly/latest/dg/setup-aws-cli.html

### Planned improvements

* Languages
    * Node
    * Java 
* Robust error handling 
* Ask questions. See you call dynamo, add to template? generate outputs? how many buckets for events? deploy template? use 'middleware' for this 
* Option to specify which kind of folders in project contain lambdas? or what kind of structure?  
* Polyglot projects?
