# -*- coding: utf-8 -*-

import urllib
import json
from floccus.models import CfnAWSResource, CfnAWSDataType, cfn_resourceref

class CfnIAMRole(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::IAM::Role")

    def _cfn_id(self):
        return self._get_api_response('RoleName') + "Role"

    @property
    def AssumeRolePolicyDocument(self):
        documentstr = urllib.unquote(self._get_api_response('AssumeRolePolicyDocument'))
        return json.loads(documentstr)

    @property
    def Path(self):
        return self._get_api_response('Path')

    @property
    def Policies(self):
        pass # A policies are always defined externally.

class CfnIAMPolicy(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::IAM::Policy")

    def _cfn_id(self):
        return self._get_api_response('PolicyName') + "Policy"

    @property
    def Groups(self):
        pass # It does not implement here yet.

    @property
    def PolicyDocument(self):
        documentstr = urllib.unquote(self._get_api_response('PolicyDocument'))
        return json.loads(documentstr)

    @property
    def PolicyName(self):
        return self._get_api_response('PolicyName')

    @property
    def Roles(self):
        return [cfn_resourceref(r + "Role") for r in self._get_api_response('Roles')]

    @property
    def Users(self):
        pass # It does not implement here yet.

class CfnIAMInstanceProfile(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::IAM::InstanceProfile")

    def _cfn_id(self):
        return self._get_api_response('InstanceProfileId')

    @property
    def Path(self):
        return self._get_api_response('Path')

    @property
    def Roles(self):
        return [cfn_resourceref(r['RoleName'] + "Role") for r in self._get_api_response('Roles')]
