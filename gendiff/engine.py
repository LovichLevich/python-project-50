from gendiff.filters.chois_filtter import get_formatter_function
from gendiff.filters.stylish import process_key
from gendiff.parser import read_file

INITIAL_DEPTH = 0


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


def generate_diff_lines(data1, data2, depth=INITIAL_DEPTH):
    keys = sorted(set(data1.keys()).union(set(data2.keys())))
    diff = []
    for key in keys:
        diff_item = process_key(key, data1, data2, depth)
        if isinstance(diff_item, list):
            diff.extend(diff_item)
        else:
            diff.append(diff_item)
    return diff


def generate_diff(file1_path, file2_path, formatter='stylish'):
    data1 = read_file(file1_path)
    data2 = read_file(file2_path)
    diff = generate_diff_lines(data1, data2)
    return format_diff(diff, formatter)
