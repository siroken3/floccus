# -*- coding: utf-8 -*-

from floccus.models import CfnAWSResource, CfnAWSDataType, cfn_resourceref

class CfnSNSTopic(CfnAWSResource):
    class _CfnSNSSubscriptionPropertyType(CfnAWSDataType):
        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)

        @property
        def Endpoint(self):
            return self._get_api_response('Endpoint')

        @property
        def Protocol(self):
            return self._get_api_response('Protocol')

    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::SNS::Topic")
        self._subscription = [self._CfnSNSSubscriptionPropertyType(sb)._cfn_expr() for sb in api_response['Subscriptions']]

    def _cfn_id(self):
        return self._get_api_response('TopicArn')

    @property
    def DisplayName(self):
        return self._get_api_response('DisplayName')

    @property
    def Subscription(self):
        return self._subscription
