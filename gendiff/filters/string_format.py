def to_string(data):
    if data is None:
        return 'null'
    elif type(data) == bool:
        return str(data).lower()
    else:
        return data


def string_format(dictionary, depth=1):
    dictionary = to_string(dictionary)
    if type(dictionary) != dict:
        return dictionary
    result = ''
    keys = list(dictionary.keys())
    keys.sort()
    for key in keys:
        item = dictionary[key]
        if type(item) == dict:
            result += (f'{depth * "    "}{key}: '
                       f'{string_format(item, depth + 1)}\n')
        else:
            if type(item) == bool:
                item = str(item).lower()
            result += f'{depth * "    "}{key}: {item}\n'
    return '{\n' + result + f'{(depth - 1) * "    "}' + '}'