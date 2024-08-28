import json as json_module

INDENT_SIZE = 4


def json(diff):
    return json_module.dumps(diff, indent=INDENT_SIZE)
