from gendiff.filters.json import gendiff_json
from gendiff.filters.plain import plain
from gendiff.filters.stylish import generate_diff_lines, stylish
from gendiff.parser import read_file

INITIAL_DEPTH = 0
DEPTH_INCREMENT = 1


def format_diff(diff, formatter='stylish'):
    if formatter == 'stylish':
        formatted_diff = stylish(diff)
    elif formatter == 'plain':
        formatted_diff = plain(diff)
    elif formatter == 'json':
        formatted_diff = gendiff_json(diff)
    else:
        raise ValueError(f"Unknown formatter: {formatter}")
    if formatter == 'plain':
        return "\n".join(formatted_diff)
    if isinstance(formatted_diff, list):
        return "{\n" + "\n".join(formatted_diff) + "\n}"
    return formatted_diff


def generate_diff(file1_path, file2_path, formatter='stylish'):
    data1 = read_file(file1_path)
    data2 = read_file(file2_path)
    diff = generate_diff_lines(data1, data2)
    return format_diff(diff, formatter)
