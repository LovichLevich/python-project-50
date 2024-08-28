import json

INDENT_SIZE = 4


def diff_json(diff):
    return json.dumps(diff, indent=INDENT_SIZE)
