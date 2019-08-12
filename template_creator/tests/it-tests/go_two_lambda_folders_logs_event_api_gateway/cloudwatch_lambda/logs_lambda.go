package main

import (
	"context"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

func HandleRequest(_ context.Context, cloudwatchLogsEvent events.SNSEvent) (string, error) {
	return "hello world", nil
}

func main() {
	lambda.Start(HandleRequest)
}
