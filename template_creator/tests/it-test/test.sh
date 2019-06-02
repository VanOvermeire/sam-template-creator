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

echo "Running cleanup of created files and stack"

cleanup ${STACK_NAME}
