#!/usr/bin/env bash

# quite simple, can be expanded later on
# TODO assert the resources that were created

function checkStatus() {
    if [[ $? -gt 0 ]]; then
        echo "$1 failed"
        exit 1
    fi
}

function cleanup() {
    rm template.yaml
    rm outputSamTemplate.yaml
    rm command_line
    aws cloudformation delete-stack --stack-name $1
}

if [[ $# -lt 1 ]]; then
    echo "The IT test needs a bucket as argument in order to run"
    exit
fi

BUCKET=$1
STACK_NAME="sam-creator-it-test"

./create.sh
location=$(pwd)
./command_line --location ${location}

checkStatus "template creator"

aws cloudformation package --template-file template.yaml --s3-bucket ${BUCKET} --output-template-file outputSamTemplate.yaml

checkStatus "packaging"

aws cloudformation deploy --template-file outputSamTemplate.yaml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM

checkStatus "deploying"

echo "Stack contains:"

aws cloudformation describe-stack-resources --stack-name ${STACK_NAME} --query StackResources

lambdas=$(aws cloudformation describe-stack-resources --stack-name arn:aws:cloudformation:eu-west-1:262438358359:stack/sam-creator-it-test/cc6c3830-856b-11e9-9ab0-0abc187d3320 --query 'StackResources[?ResourceType==`AWS::Lambda::Function`]' | jq length)
apis=$(aws cloudformation describe-stack-resources --stack-name arn:aws:cloudformation:eu-west-1:262438358359:stack/sam-creator-it-test/cc6c3830-856b-11e9-9ab0-0abc187d3320 --query 'StackResources[?ResourceType==`AWS::ApiGateway::RestApi`]' | jq length)


if [[ ${lambdas} -ne 1 ]]; then
    echo "Expected to find one lambda in results but got $lambdas."
    exit 1
elif [[ ${apis} -ne 1 ]]; then
    echo "Expected to find one api gateway in results but got $apis."
    exit 1
else
    echo "Stack created with a lambda and rest api"
fi

echo "Running cleanup of created files and stack"

cleanup ${STACK_NAME}
