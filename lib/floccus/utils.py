# -*- coding:utf-8 -*-

import os
import json
import string
import boto.ec2.tag

def iterateTags(dict_or_TagSet):
    if isinstance(dict_or_TagSet, boto.ec2.tag.TagSet):
        for key, value in dict_or_TagSet.items():
            yield (key, value)
    elif isinstance(dict_or_TagSet, boto.resultset.ResultSet):
        for astag in dict_or_TagSet:
            yield (astag.key, astag.value)
    else:
        for key, value in dict_or_TagSet:
            yield (key, value)

def to_json_list(a_list):
    if len(a_list) == 0:
        return "[]"
    else:
        return json.dumps(a_list, sort_keys=True, cls=CfnAWSResourceEncoder)

def filter_only(a_dict, include_keys):
    return dict([(k,v) for k,v in a_dict.items() if k in include_keys])

def to_cfn_tag(dict_or_TagSet):
    result = []
    for key, value in iterateTags(dict_or_TagSet):
        e = { "Key" : key, "Value" : value }
        result.append(e)
    return to_json_list(result)

def _to_cfn_ref(cfn_obj):
    return { "Ref": str(cfn_obj) }

def to_cfn_ref(cfn_obj):
    return json.dumps(_to_cfn_ref(cfn_obj), cls=CfnAWSResourceEncoder)

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

def normalize_name(name):
    return name.translate({
            ord(u'/'):u'',
            ord(u'-'):u'',
            ord(u'.'):u'',
            ord(u'-'):u''
            })

class CfnAWSResourceEncoder(json.JSONEncoder):
    def default(self, obj):
        import models
        if isinstance(obj, models.CfnAWSResource):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
