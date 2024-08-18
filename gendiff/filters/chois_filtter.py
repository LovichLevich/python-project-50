from gendiff.filters.json import gendiff_json
from gendiff.filters.plain import plain
from gendiff.filters.stylish import stylish


def get_formatter_function(formatter):
    if formatter == 'stylish':
        return stylish
    elif formatter == 'plain':
        return plain
    elif formatter == 'json':
        return gendiff_json
    else:
        raise ValueError(f"Unknown formatter: {formatter}")
