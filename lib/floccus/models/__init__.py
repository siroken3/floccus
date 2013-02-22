# -*- coding:utf-8 -*-

import json
from collections import OrderedDict

import urllib
import json
import floccus.utils as utils

exclude_pattern = {}

def load_exclude_pattern(file):
    global exclude_pattern
    with open(file) as f:
        exclude_pattern = json.load(f)

def cfn_resourceref(ref_id):
    return { 'Ref': utils.normalize_name(str(ref_id)) }

class CfnJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, CfnAWSObject):
            return o._cfn_expr()
        return json.JSONEncoder.default(self, o)

class CfnAWSObject(object):
    def _cfn_expr(self):
        raise TypeError

class CfnAWSDataType(CfnAWSObject):
    def __init__(self, api_response):
        self.__api_response = api_response

    def _has_api_response(self, key):
        return self.__api_response.has_key(key)

    def _get_api_response(self, name):
        return self.__api_response[name]

    def _resource_properties(self):
        properties = {}
        entrykeys = [p for p in dir(self) if (not p.startswith('_')) and (not self._excluded(p))]
        for entrykey in entrykeys:
            try:
                attr = getattr(self, entrykey)
                if attr is not None:
                    properties[entrykey] = attr
            except KeyError:
                pass
        return properties

    def _cfn_expr(self):
        return self._resource_properties()

    def _excluded(self, prop):
        return False


class CfnAWSResource(CfnAWSDataType):
    def __init__(self, api_response, resource_type):
        CfnAWSDataType.__init__(self, api_response)
        self._resource_type = resource_type

    def _name(self):
        return utils.normalize_name(self._cfn_id())

    def _cfn_expr(self):
        if exclude_pattern and self._excluded('*'):
            return None

        name = self._name()
        properties = self._resource_properties()
        resource_body = []
        resource_body.append(('Type', self._resource_type))
        if properties:
           resource_body.append(('Properties', properties))
        expr = (name, OrderedDict(resource_body))
        return expr

    def _excluded(self, prop):
        if not exclude_pattern:
            return False
        if self._resource_type in exclude_pattern['Type'].keys():
            if prop in exclude_pattern['Type'][self._resource_type]:
                return True
            else:
                return False
        return False
