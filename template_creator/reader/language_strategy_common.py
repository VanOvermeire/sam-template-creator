from template_creator.util.constants import HTTP_METHODS, EVENT_TYPES


# will only work for calls with strings, hence the + 1 and - 1 for getting the variable
def find_variables_in_line_of_code(result, prefix_of_get_env_var, end_of_get_env_var):
    variables = set()
    location_first_env_var = result.find(prefix_of_get_env_var)

    while location_first_env_var != -1:
        result_start_from_loc = result[location_first_env_var:]
        variable = result_start_from_loc[len(prefix_of_get_env_var) + 1: result_start_from_loc.index(end_of_get_env_var) - 1]
        variables.add(variable)

        location_first_env_var = result.find(prefix_of_get_env_var, location_first_env_var + 1)

    return variables


def find_api(split_prefix):
    method = []
    path = ''

    for line in split_prefix:
        lowecase_line = line.lower()

        if lowecase_line in HTTP_METHODS:
            method = [lowecase_line]
        elif len(lowecase_line) > 0:
            path = '{}/{}'.format(path, lowecase_line)

    if len(method) and len(path):
        method.append(path)

    return method


def find_events(lambda_event):
    events = EVENT_TYPES.keys()
    lambda_event_lower = lambda_event.lower()

    if 'cloudwatch' in lambda_event_lower:
        if 'logs' in lambda_event_lower:
            return ['CloudWatchLogs']
        return ['CloudwatchEvent']

    for event in events:
        if event.lower() in lambda_event_lower:
            return [event]
