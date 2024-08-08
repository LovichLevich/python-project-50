from gendiff.filters.stylish import generate_diff_lines, stylish
from gendiff.parser import read_file

INITIAL_DEPTH = 0
DEPTH_INCREMENT = 1


def generate_diff(file1_path, file2_path, formatter=stylish):
    data1 = read_file(file1_path)
    data2 = read_file(file2_path)
    diff = generate_diff_lines(data1, data2)
    formatted_diff = formatter(diff)
    if isinstance(formatted_diff, str):
        return formatted_diff
    elif isinstance(formatted_diff, list):
        return "{\n" + "\n".join(formatted_diff) + "\n}"
