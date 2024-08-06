import json


def convert_diff(item):
    key, status, value, depth = item
    if status == 'nested':
        return {
            "key": key,
            "status": status,
            "value": [convert_diff(subitem) for subitem in value],
            "depth": depth
        }
    return {
        "key": key,
        "status": status,
        "value": value,
        "depth": depth
    }


def gendiff_json(diff):
    json_diff = json.dumps([convert_diff(item) for item in diff], indent=1)
    return json_diff
