from gendiff.formatters.json import json
from gendiff.formatters.plain import plain
from gendiff.formatters.stylish import stylish

ERROR_MESSAGE = 'Error! Wrong output format'


def determine_format(string_format):
    if string_format == 'stylish' or not string_format:
        return stylish
    elif string_format == 'plain':
        return plain
    elif string_format == 'json':
        return json
    else:
        raise ValueError(ERROR_MESSAGE)
