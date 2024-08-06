import json  # type: ignore
import yaml  # type: ignore
from filters.stylish import stylish

INITIAL_DEPTH = 0
DEPTH_INCREMENT = 1


def read_file(file_path):
    with open(file_path, 'r') as file:
        if file_path.endswith('.json'):
            return json.load(file)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            return yaml.safe_load(file)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")


def generate_diff_lines(data1, data2, depth=0):
    keys = sorted(set(data1.keys()).union(set(data2.keys())))
    diff = []
    for key in keys:
        if key not in data2:
            diff.append((key, '-', data1[key], depth))
        elif key not in data1:
            diff.append((key, '+', data2[key], depth))
        else:
            if isinstance(data1[key], dict) and isinstance(data2[key], dict):
                nested_diff = generate_diff_lines(
                    data1[key],
                    data2[key],
                    depth + 1
                )
                diff.append((key, 'nested', nested_diff, depth))
            elif data1[key] != data2[key]:
                diff.append((key, '-', data1[key], depth))
                diff.append((key, '+', data2[key], depth))
            else:
                diff.append((key, ' ', data1[key], depth))
    return diff


def generate_diff(file1_path, file2_path, formatter=stylish):
    data1 = read_file(file1_path)
    data2 = read_file(file2_path)
    diff = generate_diff_lines(data1, data2)
    formatted_diff = formatter(diff)
    if isinstance(formatted_diff, str):
        return formatted_diff
    elif isinstance(formatted_diff, list):
        return "{\n" + "\n".join(formatted_diff) + "\n}"
