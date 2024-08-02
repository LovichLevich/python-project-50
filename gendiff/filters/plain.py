def format_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return f"'{value}'"
    return str(value)


def plain(diff, parent=''):
    lines = []
    previous_properties = set()
    for key, status, value, _ in diff:
        property_name = f"{parent}.{key}" if parent else key
        if property_name in previous_properties:
            continue
        previous_properties.add(property_name)
        if status == 'nested':
            lines.extend(process_nested(value, property_name))
        elif status == '-':
            lines.extend(process_removed(key, value, diff, property_name))
        elif status == '+':
            lines.extend(process_added(key, value, diff, property_name))
    return lines


def process_nested(value, property_name):
    return plain(value, property_name)


def process_removed(key, value, diff, property_name):
    lines = []
    next_index = find_next_index(key, diff)
    if next_index is not None:
        next_key, next_status, new_value, _ = diff[next_index]
        lines.append(
            f"Property '{property_name}' was updated. "
            f"From {format_value(value)} to {format_value(new_value)}"
        )
    else:
        lines.append(
            f"Property '{property_name}' was removed"
        )
    return lines


def find_next_index(key, diff):
    return next(
        (i for i, (k, s, _, __) in enumerate(diff)
         if k == key and s == '+'),
        None
    )


def process_added(key, value, diff, property_name):
    if any(k == key and s == '-' for k, s, _, __ in diff):
        return []
    return [
        f"Property '{property_name}' was added with value: "
        f"{format_value(value)}"
    ]
