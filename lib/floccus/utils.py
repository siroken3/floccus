# -*- coding:utf-8 -*-

import os
import json
import string
import re

def normalize_name(name):
    return re.sub(r'[/\-\._:]','', name)

def capitalize_dict(a_dict):
    return dict([ (k.capitalize(), v) for k, v in a_dict.items() ])

def valid_cfn_tag(a_tag):
    if not isinstance(a_tag, dict):
        raise ValueError(message='a_tag is not dictionary. {s}'.format(type(a_tag)))

    capitalized_tag = capitalize_dict(a_tag)
    if 'Key' in capitalized_tag:
        key = capitalized_tag['Key']
    else:
        raise ValueError(message='a_tag is invalid dictionary')

    if key.startswith('aws:'):
        return False

    return True

def flatten(orgdict, column):
    import copy
    pivot = orgdict[column]
    del(orgdict[column])
    result = []
    for p in pivot:
        copied = copy.deepcopy(orgdict)
        copied.update(p)
        result.append(copied)
    return result

def groupby(dict_list, group_by, other_column):
    import itertools
    result = []
    for group_by_key, group_itr in itertools.groupby(dict_list, lambda x: x[group_by]):
        e = {}
        e[group_by] = group_by_key
        e[other_column] = [g[other_column] for g in list(group_itr)]
        result.append(e)
    return result
