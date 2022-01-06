import sys


def table_to_dict(inp):
    lines = inp.split('\n')
    ret = []
    keys = []
    for i, l in enumerate(lines):
        if i == 0:
            keys = [_i.strip() for _i in l.split('|')]
        elif i == 1:
            continue
        else:
            ret.append({keys[_i]: v.strip() for _i, v in enumerate(l.split('|'))if (_i > 0) and (_i < len(keys)-1)})
    return ret


if __name__ == '__main__':
    my_str = '''| Some Title | Some Description             | Some Number |
    |------------|------------------------------|-------------|
    | Dark Souls | This is a fun game           | 5           |
    | Blood borne | This one is even better      | 2           |'''

    unit_test = table_to_dict(my_str)
    if type(unit_test[0]) == dict:
        sys.exit(0)
    else:
        sys.exit(1)
