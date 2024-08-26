import json

from gendiff.constants import INDENT_SIZE


def diff_json(diff):
    result = json.dumps(diff, indent=INDENT_SIZE)
    return result
