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


def get_property_name(parent, key):
    return f"{parent}.{key}" if parent else key


def is_property_processed(property_name, previous_properties):
    return property_name in previous_properties


def add_property_to_set(property_name, previous_properties):
    previous_properties.add(property_name)


def process_status(status, key, value, diff, property_name):
    status_handlers = {
        'nested': handle_nested,
        '-': handle_removed,
        '+': handle_added
    }
    handler = status_handlers.get(status, lambda *args: [])
    return handler(key, value, diff, property_name)


def handle_nested(key, value, diff, property_name):
    return plain(value, property_name)


def handle_removed(key, value, diff, property_name):
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


def handle_added(key, value, diff, property_name):
    if not any(k == key and s == '-' for k, s, _, __ in diff):
        return [
            f"Property '{property_name}' was added with value: "
            f"{format_value(value)}"
        ]
    return []


def process_diff_item(diff_item, diff, parent, previous_properties):
    key, status, value, _ = diff_item
    property_name = get_property_name(parent, key)
    if is_property_processed(property_name, previous_properties):
        return []
    add_property_to_set(property_name, previous_properties)
    return process_status(status, key, value, diff, property_name)


def find_next_index(key, diff):
    return next(
        (i for i, (k, s, _, __) in enumerate(diff)
         if k == key and s == '+'),
        None
    )


def plain(diff, parent=''):
    lines = []
    previous_properties = set()
    for diff_item in diff:
        lines.extend(process_diff_item(
            diff_item, diff, parent, previous_properties
        ))
    return lines
