INDENT_SIZE = 4
INITIAL_DEPTH = 0
DEPTH_INCREMENT = 1


def conv_string(value):
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, str):
        return f'"{value}"'
    return str(value)


def process_value(value):
    if isinstance(value, str) and not (
        value.isdigit() or value in {'true', 'false', 'null'}
    ):
        return value
    return conv_string(value)


def process_nested(key, value, depth, indent, lines):
    lines.append(f"{indent}    {key}: {{")
    lines.extend(stylish(value, depth + DEPTH_INCREMENT))
    lines.append(f"{indent}    }}")


def generate_diff_lines(data1, data2, depth=INITIAL_DEPTH):
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
                    depth + DEPTH_INCREMENT
                )
                diff.append((key, 'nested', nested_diff, depth))
            elif data1[key] != data2[key]:
                diff.append((key, '-', data1[key], depth))
                diff.append((key, '+', data2[key], depth))
            else:
                diff.append((key, ' ', data1[key], depth))
    return diff


def process_dict(key, value, depth, symbol, indent, lines):
    lines.append(f"{indent}  {symbol} {key}: {{")
    nested_lines = stylish(
        generate_diff_lines(value, {}, depth + DEPTH_INCREMENT),
        depth + DEPTH_INCREMENT
    )
    if symbol in ['-', '+']:
        nested_lines = [
            line.replace('+ ', '  ').replace('- ', '  ')
            for line in nested_lines
        ]
    lines.extend(nested_lines)
    lines.append(f"{indent}    }}")


def process_line(key, symbol, value_str, depth, indent, lines):
    line = f"{indent}  {symbol} {key}: {value_str}"
    if depth > INITIAL_DEPTH and symbol not in ['-', '+']:
        line = f"{indent}    {key}: {value_str}"
    lines.append(line)


def stylish(diff, depth=INITIAL_DEPTH):
    indent = ' ' * INDENT_SIZE * depth
    lines = []
    for key, status, value, value_depth in diff:
        symbol = '-' if status == '-' else '+' if status == '+' else ' '
        if status == 'nested':
            process_nested(key, value, depth, indent, lines)
        elif isinstance(value, dict):
            process_dict(key, value, depth, symbol, indent, lines)
        else:
            value_str = process_value(value)
            process_line(key, symbol, value_str, depth, indent, lines)
    return lines
