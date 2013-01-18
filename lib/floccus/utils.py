# -*- coding:utf-8 -*-

import os
import json
import boto.ec2.tag

def iterateTags(dict_or_TagSet):
    items = dict_or_TagSet.items() if isinstance(dict_or_TagSet, boto.ec2.tag.TagSet) else dict_or_TagSet
    for key, value in items:
        yield (key, value)

def to_json_list(a_list):
    return "[]" if len(a_list) == 0 else json.dumps(a_list, sort_keys=True)

def to_cfn_tag(dict_or_TagSet):
    result = []
    for key, value in iterateTags(dict_or_TagSet):
        e = { "Key" : key, "Value" : value }
        result.append(e)
    return to_json_list(result)

def _to_cfn_ref(cfn_obj):
    return { "Ref": str(cfn_obj) }

def to_cfn_ref(cfn_obj):
    return json.dumps(_to_cfn_ref(cfn_obj))

def to_cfn_ref_list(cfn_list):
    return to_json_list([ _to_cfn_ref(e) for e in cfn_list])

def get_aws_key(access_key=None, secret_key=None):
    if access_key is None:
        if os.environ.get('AWS_ACCESS_KEY') is None:
            aws_access_key = None
        else:
            aws_access_key = os.environ.get('AWS_ACCESS_KEY')
    else:
        aws_access_key = access_key

    if secret_key is None:
        if os.environ.get('AWS_SECRET_KEY') is None:
            aws_secret_key = None
        else:
            aws_secret_key = os.environ.get('AWS_SECRET_KEY')
    else:
        aws_secret_key = secret_key

    return (aws_access_key, aws_secret_key)
