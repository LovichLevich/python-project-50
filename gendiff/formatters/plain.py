from gendiff.string_format import string_format

DEPTH_INCREMENT = 1


def to_string(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return string_format(value)


def get_path_plain(previous_path, new_part):
    new_path = f'{previous_path}.{new_part}'[DEPTH_INCREMENT:]
    return new_path


def gen_text_diff_plain_real(diff, path=''):
    result = ''
    for key in diff['keys']:
        if key in diff['removed'].keys():
            result += f"Property '{get_path_plain(path, key)}' was removed\n"
        elif key in diff['added'].keys():
            item = diff['added'][key]
            result += (f"Property '{get_path_plain(path, key)}' was added with"
                       f" value: {to_string(item)}\n")
        elif key in diff['nested'].keys():
            result += gen_text_diff_plain_real(
                diff['nested'][key], path + f'.{key}'
            )
        elif key in diff['changed'].keys():
            was = to_string(diff['changed'][key]['old_value'])
            now = to_string(diff['changed'][key]['new_value'])
            result += (f"Property '{get_path_plain(path, key)}' was "
                       f"updated. From {was} to {now}\n")
    return result


def plain(diff):
    plain_diff = gen_text_diff_plain_real(diff)
    return plain_diff.rstrip()
