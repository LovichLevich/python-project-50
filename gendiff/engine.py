import json

file1_path = '/python-project-50/gendiff/dir_with_jsons/file1.json'
file2_path = '/python-project-50/gendiff/dir_with_jsons/file2.json'


def convert_value_to_string(value):
    if value is None:
        return "none"
    elif isinstance(value, bool):
        return str(value).lower()
    return value


def generate_diff(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)
    
        keys = set(data1.keys()).union(set(data2.keys()))
    
        diff_lines = []

    for key in sorted(keys):
        if key not in data2:
            diff_lines.append(f"  - {key}: {convert_value_to_string(data1[key])}")
        elif key not in data1:
            diff_lines.append(f"  + {key}: {convert_value_to_string(data2[key])}")
        else:
            if data1[key] != data2[key]:
                diff_lines.append(f"  - {key}: {convert_value_to_string(data1[key])}")
                diff_lines.append(f"  + {key}: {convert_value_to_string(data2[key])}")
            else:
                diff_lines.append(f"    {key}: {convert_value_to_string(data1[key])}")

    diff_result = "{\n" + "\n".join(diff_lines) + "\n}"
    
    return diff_result
