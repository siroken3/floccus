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
