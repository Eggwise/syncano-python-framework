import os, re, json, urllib


# SOURCE ITERATOR
def get_parent(path):
    parent, current = os.path.split(path)

    dirs = []
    files = []
    for item in os.listdir(path):
        if os.path.isdir(item):
            dirs.append(item)
        else:
            files.append(item)
    return parent, dirs, files


def walk_upwards(start_path):
    new_path = os.path.realpath(start_path)
    while True:
        parent, dirs, files = get_parent(new_path)
        if new_path == parent:
            break

        yield new_path, dirs, files
        new_path = parent


def find_dirs(start_path, regex, upwards=True, find_first=True, stop=None):
    found_paths = []
    level = 0
    for matches in find_dirs_iterator(start_path, regex=regex, upwards=upwards):
        level += 1
        # print(matches)
        if stop is not None:
            if level == stop:
                return found_paths

        if matches:
            found_paths += [os.path.realpath(i) for i in matches]

            if find_first:
                return found_paths

    return found_paths


def find_dirs_iterator(start_path, regex, upwards=True):
    if upwards:
        walk_iterator = walk_upwards
    else:
        walk_iterator = os.walk

    for path, dirs, files in walk_iterator(start_path):
        # print('gozer', path, dirs, files)
        matches = [os.path.join(path, i) for i in dirs + files if re.match(regex, str(i))]
        # print(matches)
        yield matches


# SOURCE ITERATOR





# MERGE FUNCTION FOR MERGING OF CONFIGS
# merge dict 2 in dict 1 ! (dict2 overides 1 , if items cant be merged)
def merge(dict_1: dict, dict_2: dict):
    merged_dict = {**dict_1, **dict_2}

    for dict_1_key, dict_1_val in dict_1.items():
        if dict_1_key not in dict_2:
            continue
        dict_2_val = dict_2[dict_1_key]
        merged_value = dict_2_val
        if type(dict_1_val) != type(dict_2_val):
            ##not the same types
            print('trying to merge values of dict with different types, key: {0}, value types: {1} , {2}'.format(
                dict_1_key, type(dict_1_val), type(dict_2_val)))
            merged_value = dict_2_val

        if isinstance(dict_1_val, dict):
            merged_value = merge(dict_1_val, dict_2_val)

        if isinstance(dict_1_val, list):
            merged_value = [*dict_1_val, *dict_2_val]

        merged_dict[dict_1_key] = merged_value

    return merged_dict


##PRETTY REPRESENTATION
def pretty_print(cls):
    def repr_func(object):
        the_repr = '{type}:\t({dict})'.format(type=type(object), dict=object.__dict__)
        return the_repr
    cls.__repr__ = repr_func
    return cls




class LOG_CONSTANTS:

    REGION = '========= {0} ========='
    LINE = '\n{0}'
    REGION_IDENTIFIER = '\n\n'


    INDEXED_FILE_TEMPLATE = \
'''
Indexed fil
{REGION}
file: {0}



'''