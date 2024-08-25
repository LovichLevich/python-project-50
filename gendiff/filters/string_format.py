def to_string(data):
    if data is None:
        return 'null'
    elif isinstance(data, bool):
        return str(data).lower()
    else:
        return data


def string_format(dictionary, depth=1):
    dictionary = to_string(dictionary)
    if not isinstance(dictionary, dict):
        return dictionary
    result = ''
    keys = sorted(dictionary.keys())
    indent = '    ' * depth
    for key in keys:
        item = dictionary[key]
        if isinstance(item, dict):
            result += f'{indent}{key}: {string_format(item, depth + 1)}\n'
        else:
            if isinstance(item, bool):
                item = str(item).lower()
            result += f'{indent}{key}: {item}\n'
    return '{\n' + result + f'{"    " * (depth - 1)}}}'
