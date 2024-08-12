def format_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)


def process_diff_item(key, status, value, diff, parent, previous_properties):
    property_name = f"{parent}.{key}" if parent else key
    if property_name in previous_properties:
        return []
    previous_properties.add(property_name)
    if status == 'nested':
        return process_nested(value, property_name)
    if status == '-':
        return process_removed(key, value, diff, property_name)
    if status == '+':
        return process_added(key, value, diff, property_name)
    return []


def plain(diff, parent=''):
    lines = []
    previous_properties = set()
    for key, status, value, _ in diff:
        lines.extend(process_diff_item(
            key, status, value, diff, parent, previous_properties
        ))
    return lines


def process_nested(value, property_name):
    return plain(value, property_name)


def process_removed(key, value, diff, property_name):
    lines = []
    next_index = find_next_index(key, diff)
    if next_index is not None:
        _, _, new_value, _ = diff[next_index]
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
    if not any(k == key and s == '-' for k, s, _, __ in diff):
        return [
            f"Property '{property_name}' was added with value: "
            f"{format_value(value)}"
        ]
    return []
