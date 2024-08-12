def format_value(value):
    type_map = {
        dict: '[complex value]',
        bool: str(value).lower(),
        type(None): 'null',
        int: str(value),
        float: str(value),
        str: f"'{value}'"
    }
    return type_map.get(type(value), str(value))


def process_diff_item(key, status, value, diff, parent, previous_properties):
    property_name = f"{parent}.{key}" if parent else key
    if property_name in previous_properties:
        return []
    previous_properties.add(property_name)
    status_map = {
        'nested': process_nested,
        '-': process_removed,
        '+': process_added
    }
    return status_map.get(status, lambda *args: [])(
        key, value, diff, property_name, previous_properties
    )


def process_nested(key, value, diff, property_name, previous_properties):
    return plain(value, property_name)


def process_removed(key, value, diff, property_name, previous_properties):
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


def process_added(key, value, diff, property_name, previous_properties):
    if not any(k == key and s == '-' for k, s, _, __ in diff):
        return [
            f"Property '{property_name}' was added with value: "
            f"{format_value(value)}"
        ]
    return []


def find_next_index(key, diff):
    return next(
        (i for i, (k, s, _, __) in enumerate(diff)
         if k == key and s == '+'),
        None
    )


def plain(diff, parent=''):
    lines = []
    previous_properties = set()
    for key, status, value, _ in diff:
        lines.extend(process_diff_item(
            key, status, value, diff, parent, previous_properties
        ))
    return lines
