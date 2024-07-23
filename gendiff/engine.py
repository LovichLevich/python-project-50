import json
import yaml


def conv_string(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return "null"
    return str(value)


def read_file(file_path):
    with open(file_path, 'r') as file:
        if file_path.endswith('.json'):
            return json.load(file)
        elif file_path.endswith('.yaml'):
            return yaml.safe_load(file)
        else:
            raise ValueError("Unsupported file format")


def generate_diff_lines(data1, data2):
    keys = set(data1.keys()).union(set(data2.keys()))
    diff_lines = []
    for key in sorted(keys):
        if key not in data2:
            diff_lines.append(f"  - {key}: {conv_string(data1[key])}")
        elif key not in data1:
            diff_lines.append(f"  + {key}: {conv_string(data2[key])}")
        else:
            if data1[key] != data2[key]:
                diff_lines.append(f"  - {key}: {conv_string(data1[key])}")
                diff_lines.append(f"  + {key}: {conv_string(data2[key])}")
            else:
                diff_lines.append(f"    {key}: {conv_string(data1[key])}")
    return diff_lines


def generate_diff(file1_path, file2_path):
    data1 = read_file(file1_path)
    data2 = read_file(file2_path)
    diff_lines = generate_diff_lines(data1, data2)
    diff_result = "{\n" + "\n".join(diff_lines) + "\n}"
    return diff_result
