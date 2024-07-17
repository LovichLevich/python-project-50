import json
import yaml

def convert_value_to_string(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return "null"
    return str(value)

def generate_diff(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        if file1_path.endswith('.json') and file2_path.endswith('.json'):
            data1 = json.load(file1)
            data2 = json.load(file2)
        elif file1_path.endswith('.yaml') and file2_path.endswith('.yaml'):
            data1 = yaml.safe_load(file1)
            data2 = yaml.safe_load(file2)
        else:
            raise ValueError("Unsupported file format")
    
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
