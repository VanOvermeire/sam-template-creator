import unittest

from template_creator.reader.GoStrategy import GoStrategy


class TestGoStrategy(unittest.TestCase):
    def setUp(self):
        self.lines = ['package main\n', '\n', 'import (\n', '\t"context"\n', '\t"fmt"\n', '\t"github.com/aws/aws-lambda-go/events"\n', '\t"github.com/aws/aws-lambda-go/lambda"\n', '\t"os"\n', ')\n',
                      '\n', 'var dbClient *db.Client\n', '\n', 'func init() {\n', '\tdbClient = db.SetupDynamoDBClient(os.Getenv("REGION"), os.Getenv("TABLE_NAME"))\n', '}\n', '\n',
                      'func HandleRequest(_ context.Context, event events.APIGatewayProxyRequest) (Response, error) {\n', '// some message\n', '\treturn handleAdd(dbClient, event)\n', '}\n', '\n',
                      'func main() {\n', '\tlambda.Start(HandleRequest)\n', '}\n']
        self.strategy = GoStrategy()
        self.hander_line = 'func HandleRequest(_ context.Context, s3event events.APIGatewayProxyRequest) (Response, error) {'

    def test_is_handler_tabs(self):
        is_handler, line = self.strategy.is_handler_file(self.lines)

        self.assertTrue(is_handler)
        self.assertEqual(line, 'func HandleRequest(_ context.Context, event events.APIGatewayProxyRequest) (Response, error) {\n')

    def test_is_handler_spaces(self):
        lines = ['package main\n', '\n', 'import (\n', '\t"context"\n', '\t"fmt"\n', '\t"github.com/aws/aws-lambda-go/events"\n', '\t"github.com/aws/aws-lambda-go/lambda"\n', '\t"os"\n', ')\n',
                 'func HandleRequest(_ context.Context, event events.APIGatewayProxyRequest) (Response, error) {\n', '// some message\n', '\treturn handleAdd(dbClient, event)\n', '}\n', '\n',
                 'func main() {\n', '  lambda.Start(HandleRequest)\n', '}\n']

        is_handler, line = self.strategy.is_handler_file(lines)

        self.assertTrue(is_handler)
        self.assertEqual(line, 'func HandleRequest(_ context.Context, event events.APIGatewayProxyRequest) (Response, error) {\n')

    def test_is_not_handler(self):
        lines = ['package main\n', '\n', 'import (\n', '\t"context"\n', '\t"fmt"\n', '\t"github.com/aws/aws-lambda-go/events"\n', '\t"github.com/aws/aws-lambda-go/lambda"\n', '\t"os"\n', ')\n',
                 'func HandleRequest(_ context.Context, event events.APIGatewayProxyRequest) (Response, error) {\n', '// some message\n', '\treturn handleAdd(dbClient, event)\n', '}\n', '\n',
                 'func main() {\n', ' fmt.Println("Stuff")\n', '}\n']

        is_handler, line = self.strategy.is_handler_file(lines)

        self.assertFalse(is_handler)

    def test_build_handler(self):
        result = self.strategy.build_handler('/some/location/dir_of_lambda', '/some/location/dir_of_lambda/file.py', self.hander_line)

        self.assertEqual(result, 'main')

    def test_find_events(self):
        result = self.strategy.find_events(self.hander_line)

        self.assertEqual(result, ['S3'])

    def test_find_events_with_underscore_in_name_event(self):
        handler_line = 'func HandleRequest(_ context.Context, s3event events.APIGatewayProxyRequest) (Response, error) {\n'

        result = self.strategy.find_events(handler_line)

        self.assertEqual(result, ['S3'])

    def test_find_events_no_event(self):
        handler_line = 'func HandleRequest(_ context.Context, event events.APIGatewayProxyRequest) (Response, error) {'

        result = self.strategy.find_events(handler_line)

        self.assertIsNone(result)

    def test_find_events_no_arguments(self):
        handler_line = 'func HandleRequest() error {'

        result = self.strategy.find_events(handler_line)

        self.assertIsNone(result)

    def test_find_api_no_api(self):
        result = self.strategy.find_api(self.hander_line)

        self.assertEqual(result, [])

    def test_find_api_simple_with_method_first(self):
        handler_line = 'func PutAddRequest(_ context.Context, event events.APIGatewayProxyRequest) (Response, error) {'

        result = self.strategy.find_api(handler_line)

        self.assertEqual(result, ['put', '/add'])

    def test_find_api_simple_with_method_second(self):
        handler_line = 'func AddPostRequest() (Response, error) {'

        result = self.strategy.find_api(handler_line)

        self.assertEqual(result, ['post', '/add'])

    def test_find_api_multiple_levels_with_method_first(self):
        handler_line = 'func PutAddHelloRequest(_ context.Context, event events.APIGatewayProxyRequest) error {'

        result = self.strategy.find_api(handler_line)

        self.assertEqual(result, ['put', '/add/hello'])

    def test_find_env_variables(self):
        result = self.strategy.find_env_variables(self.lines)

        self.assertCountEqual(result, ['TABLE_NAME', 'REGION'])

    def test_find_roles_no_roles(self):
        result = self.strategy.find_role(self.lines)

        self.assertCountEqual(result, [])

    def test_find_roles(self):
        lines = ['package main\n', '\n', 'import (\n', '\t"context"\n', '\t"fmt"\n', '\t"github.com/aws/aws-lambda-go/events"\n', '\t"github.com/aws/aws-lambda-go/lambda"\n',
                 '\t"github.com/aws/aws-sdk-go/service/s3"\n', '\t"go-reservations/db"\n', '\t"os"\n', ')\n', '\n', 'var dbClient *db.Client\n', '\n', 'func init() {\n',
                 'func HandleRequest(_ context.Context, event events.APIGatewayProxyRequest) (Response, error) {\n', '\tfmt.Println("Received ", event) // remove, temporary logging\n',
                 '\treturn handleAdd(dbClient, event)\n', '}\n', '\n', 'func main() {\n', '\tlambda.Start(HandleRequest)\n', '}\n']

        result = self.strategy.find_role(lines)

        self.assertCountEqual(result, ['s3:*'])
