import json

INDENT_SIZE = 4


def diff_json(diff):
    result = json.dumps(diff, indent=INDENT_SIZE)
    return result
