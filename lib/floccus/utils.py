# -*- coding:utf-8 -*-

import os
import json
import string
import re

_default_type_order = [
    "AWS::EC2::VPC",
    "AWS::EC2::InternetGateway",
    "AWS::EC2::VPCGatewayAttachment",
    "AWS::EC2::Subnet",
    "AWS::EC2::SecurityGroup",
    "AWS::EC2::RouteTable",
    "AWS::EC2::SubnetRouteTableAssociation",
    "AWS::EC2::Instance",
    "AWS::EC2::Route",
    "AWS::ElasticLoadBalancing::LoadBalancer",
    "AWS::AutoScaling::LaunchConfiguration",
    "AWS::AutoScaling::ScalingPolicy",
    "AWS::AutoScaling::AutoScalingGroup",
    "AWS::RDS::DBInstance",
    "AWS::SNS::Topic",
]

def normalize_name(name):
    return re.sub(r'[/\-\._:]','', name)

def capitalize_dict(a_dict):
    return dict([ (k.capitalize(), v) for k, v in a_dict.items() ])

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

def sort_by_cfn_resource_type(a_list, type_order=_default_type_order):
    import sys
    def _key_func(e):
        if e[1]['Type'] in type_order:
            return type_order.index(e[1]['Type'])
        else:
            return sys.maxint

    return sorted(a_list, key=_key_func)
