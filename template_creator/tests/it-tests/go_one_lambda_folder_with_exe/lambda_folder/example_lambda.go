package main

import (
	"context"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

func HandleRequest(_ context.Context, event events.SNSEvent) (string, error) {
	return "OK", nil
}

func main() {
	lambda.Start(HandleRequest)
}
