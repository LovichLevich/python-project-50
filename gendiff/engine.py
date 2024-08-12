from gendiff.filters.json import gendiff_json
from gendiff.filters.plain import plain
from gendiff.filters.stylish import generate_diff_lines, stylish
from gendiff.parser import read_file


def get_formatter_function(formatter):
    if formatter == 'stylish':
        return stylish
    elif formatter == 'plain':
        return plain
    elif formatter == 'json':
        return gendiff_json
    else:
        raise ValueError(f"Unknown formatter: {formatter}")


def format_diff_result(formatted_diff, formatter):
    if formatter == 'plain':
        return "\n".join(formatted_diff)
    if isinstance(formatted_diff, list):
        return "{\n" + "\n".join(formatted_diff) + "\n}"
    return formatted_diff


def format_diff(diff, formatter='stylish'):
    formatter_function = get_formatter_function(formatter)
    formatted_diff = formatter_function(diff)
    return format_diff_result(formatted_diff, formatter)


def generate_diff(file1_path, file2_path, formatter='stylish'):
    data1 = read_file(file1_path)
    data2 = read_file(file2_path)
    diff = generate_diff_lines(data1, data2)
    return format_diff(diff, formatter)
