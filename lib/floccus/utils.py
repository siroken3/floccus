# -*- coding:utf-8 -*-

import os
import json
import string

def normalize_name(name):
    return name.translate({
            ord(u'/'):u'',
            ord(u'-'):u'',
            ord(u'.'):u'',
            ord(u'-'):u''
            })

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
