# -*- coding:utf-8 -*-

from floccus.models import CfnAWSResource, CfnAWSDataType, cfn_resourceref

class CfnRDSDBInstance(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::RDS::DBInstance")
