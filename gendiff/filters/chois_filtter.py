from gendiff.constants import ERROR_MESSAGE
from gendiff.filters.json import diff_json
from gendiff.filters.plain import plain
from gendiff.filters.stylish import stylish


def get_format(string_format):
    if string_format == 'stylish' or not string_format:
        return stylish
    elif string_format == 'plain':
        return plain
    elif string_format == 'json':
        return diff_json
    else:
        raise ValueError(ERROR_MESSAGE)
