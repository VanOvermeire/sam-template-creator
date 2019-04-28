#!/usr/bin/env bash

# TODO this still uses the old way - running with executable. Instead do a local pip install in a virtual env and use pip to create template
# quite simple, can be expanded later on

function checkStatus() {
    if [[ $? -gt 0 ]]; then
        echo "$1 failed"
        exit 1
    fi
}

if [[ $# -lt 1 ]]; then
    echo "The IT test needs a bucket as argument in order to run"
    exit
fi

BUCKET=$1
STACK_NAME="sam-creator-it-test"

# maybe create executable before every run?
cp ../../dist/template_creator .

location=$(pwd)
./template_creator --location ${location}

checkStatus "template creator"

aws cloudformation package --template-file template.yaml --s3-bucket ${BUCKET} --output-template-file outputSamTemplate.yaml

checkStatus "packaging"

aws cloudformation deploy --template-file outputSamTemplate.yaml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM

checkStatus "deploying"

echo "Running cleanup of created files and stack"

rm template.yaml
rm outputSamTemplate.yaml
rm template_creator
aws cloudformation delete-stack --stack-name ${STACK_NAME}
