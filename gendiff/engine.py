import json  # type: ignore
import yaml  # type: ignore


def conv_string(value):
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, str):
        return f'"{value}"'
    return str(value)


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
                nested_diff = generate_diff_lines(data1[key], data2[key], depth + 1)
                diff.append((key, 'nested', nested_diff, depth))
            elif data1[key] != data2[key]:
                diff.append((key, '-', data1[key], depth))
                diff.append((key, '+', data2[key], depth))
            else:
                diff.append((key, ' ', data1[key], depth))
    return diff


def stylish(diff, depth=0):
    indent = ' ' * 4 * depth
    lines = []
    for key, status, value, value_depth in diff:
        if status == 'nested':
            lines.append(f"{indent}    {key}: {{")
            lines.extend(stylish(value, depth + 1))
            lines.append(f"{indent}    }}")
        else:
            symbol = '-' if status == '-' else '+' if status == '+' else ' '
            if isinstance(value, dict):
                lines.append(f"{indent}  {symbol} {key}: {{")
                nested_lines = stylish(generate_diff_lines(value, {}, depth + 1), depth + 1)
                if symbol in ['-', '+']:
                    nested_lines = [line.replace('+ ', '  ').replace('- ', '  ') for line in nested_lines]
                lines.extend(nested_lines)
                lines.append(f"{indent}    }}")
            else:
                if isinstance(value, str) and not (value.isdigit() or value in {'true', 'false', 'null'}):
                    value_str = value
                else:
                    value_str = conv_string(value)
                line = f"{indent}  {symbol} {key}: {value_str}"
                if depth > 0 and symbol not in ['-', '+']:
                    line = f"{indent}    {key}: {value_str}"
                lines.append(line)
    return lines


def generate_diff(file1_path, file2_path, formatter=stylish):
    data1 = read_file(file1_path)
    data2 = read_file(file2_path)
    diff = generate_diff_lines(data1, data2)
    formatted_diff = formatter(diff)
    return "{\n" + "\n".join(formatted_diff) + "\n}"
