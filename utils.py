import os
import itertools


def merge_dicts(dict1, dict2):
    return dict(itertools.chain(
        dict1.iteritems(),
        dict2.iteritems()
    ))


def usual_config_files(base_name, sysdir='/etc'):
    hidden = '.' + base_name

    system_file = os.path.join(sysdir, base_name)
    user_file = os.path.join('~', hidden)
    local_file = os.path.join('.', hidden)
    return (system_file, user_file, local_file)
