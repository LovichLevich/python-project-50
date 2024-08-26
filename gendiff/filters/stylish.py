from gendiff.constants import DEPTH_INCREMENT
from gendiff.filters.string_format import string_format


def gen_tree_changed(item, key, depth):
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
            result += gen_tree_changed(item, key, depth)
        else:
            item = diff['nested'][key]
            result += (f'{depth * "    "}{key}: '
                       f'{stylish(item, depth + DEPTH_INCREMENT)}\n')

    result = '{\n' + result + f'{(depth - DEPTH_INCREMENT) * "    "}' + '}'
    return result
