from helper_file import a_helper


def some_handler(s3_event, context):
    print("Received {}".format(s3_event))
    return a_helper()
