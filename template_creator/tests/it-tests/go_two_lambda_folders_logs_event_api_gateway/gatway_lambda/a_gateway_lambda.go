package main

import (
	"context"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
)

func PostHelloRequest(_ context.Context, event events.SNSEvent) (string, error) {
	awsSession, _ := session.NewSession(&aws.Config{Region: aws.String("eu-west-1")})
	db := dynamodb.New(awsSession)

	return "hello world", nil
}

func main() {
	lambda.Start(PostHelloRequest)
}
