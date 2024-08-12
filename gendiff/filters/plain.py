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


def process_status(context):
    status_handlers = {
        'nested': handle_nested,
        '-': handle_removed,
        '+': handle_added
    }
    handler = status_handlers.get(context['status'], lambda *args: [])
    return handler(context)


def handle_nested(context):
    return plain(context['value'], context['property_name'])


def handle_removed(context):
    lines = []
    next_index = find_next_index(context['key'], context['diff'])
    if next_index is not None:
        _, _, new_value, _ = context['diff'][next_index]
        lines.append(
            f"Property '{context['property_name']}' was updated. "
            f"From {format_value(context['value'])} to "
            f"{format_value(new_value)}"
        )
    else:
        lines.append(
            f"Property '{context['property_name']}' was removed"
        )
    return lines


def handle_added(context):
    if not any(
        k == context['key'] and s == '-'
        for k, s, _, __ in context['diff']
    ):
        return [
            f"Property '{context['property_name']}' was added with value: "
            f"{format_value(context['value'])}"
        ]
    return []


def process_diff_item(diff_item, diff, parent, previous_properties):
    key, status, value, _ = diff_item
    property_name = get_property_name(parent, key)
    if is_property_processed(property_name, previous_properties):
        return []
    add_property_to_set(property_name, previous_properties)
    context = {
        'status': status,
        'key': key,
        'value': value,
        'diff': diff,
        'property_name': property_name
    }
    return process_status(context)


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
