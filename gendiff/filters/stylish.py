from gendiff.engine import generate_diff_lines


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
    lines.extend(stylish(value, depth + 1))
    lines.append(f"{indent}    }}")


def process_dict(key, value, depth, symbol, indent, lines):
    lines.append(f"{indent}  {symbol} {key}: {{")
    nested_lines = stylish(generate_diff_lines(value, {}, depth + 1), depth + 1)
    if symbol in ['-', '+']:
        nested_lines = [
            line.replace('+ ', '  ').replace('- ', '  ')
            for line in nested_lines
        ]
    lines.extend(nested_lines)
    lines.append(f"{indent}    }}")


def process_line(key, symbol, value_str, depth, indent, lines):
    line = f"{indent}  {symbol} {key}: {value_str}"
    if depth > 0 and symbol not in ['-', '+']:
        line = f"{indent}    {key}: {value_str}"
    lines.append(line)


def stylish(diff, depth=0):
    indent = ' ' * 4 * depth
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
