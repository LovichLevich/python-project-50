import json


def diff_json(diff):
    result = json.dumps(diff, indent=4)
    return result
