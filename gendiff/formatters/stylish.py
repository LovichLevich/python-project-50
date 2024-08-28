DEPTH_INCREMENT = 1


def to_string(data):
    if data is None:
        return 'null'
    elif isinstance(data, bool):
        return str(data).lower()
    else:
        return data


def string_format(dictionary, depth=DEPTH_INCREMENT):
    dictionary = to_string(dictionary)
    if not isinstance(dictionary, dict):
        return dictionary
    result = ''
    keys = sorted(dictionary.keys())
    indent = '    ' * depth
    for key in keys:
        item = dictionary[key]
        if isinstance(item, dict):
            result += (
                f'{indent}{key}: '
                f'{string_format(item, depth + DEPTH_INCREMENT)}\n'
            )
        else:
            if isinstance(item, bool):
                item = str(item).lower()
            result += f'{indent}{key}: {item}\n'
    return '{\n' + result + f'{"    " * (depth - DEPTH_INCREMENT)}}}'


def generate_tree_changed(item, key, depth):
    result = ''
    item1 = string_format(item['old_value'], depth + DEPTH_INCREMENT)
    item2 = string_format(item['new_value'], depth + DEPTH_INCREMENT)
    result += f'{(depth - DEPTH_INCREMENT) * "    "}  - {key}: {item1}\n'
    result += f'{(depth - DEPTH_INCREMENT) * "    "}  + {key}: {item2}\n'
    return result


def stylish(diff, depth=DEPTH_INCREMENT):
    result = ''
    for key in diff['keys']:
        if key in diff['unchanged'].keys():
            item = string_format(
                diff["unchanged"][key], depth + DEPTH_INCREMENT
            )
            result += f'{depth * "    "}{key}: {item}\n'
        elif key in diff['removed'].keys():
            item = string_format(diff["removed"][key], depth + DEPTH_INCREMENT)
            result += f'{(depth - DEPTH_INCREMENT) * "    "}  - {key}: {item}\n'
        elif key in diff['added'].keys():
            item = string_format(diff["added"][key], depth + DEPTH_INCREMENT)
            result += f'{(depth - DEPTH_INCREMENT) * "    "}  + {key}: {item}\n'
        elif key in diff['changed']:
            item = diff['changed'][key]
            result += generate_tree_changed(item, key, depth)
        else:
            item = diff['nested'][key]
            result += (f'{depth * "    "}{key}: '
                       f'{stylish(item, depth + DEPTH_INCREMENT)}\n')

    result = '{\n' + result + f'{(depth - DEPTH_INCREMENT) * "    "}' + '}'
    return result
