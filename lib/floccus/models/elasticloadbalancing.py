# -*- coding:utf-8 -*-

from floccus.models import CfnAWSResource, CfnAWSDataType, cfn_resourceref

class CfnElasticLoadBalancingLoadBalancer(CfnAWSResource):
    class _AppCookieStickinessPolicy(CfnAWSDataType):
        def __init__(self, api_response):
            pass

        @property
        def CookieName(self):
            pass

        @property
        def PolicyName(self):
            pass

    class _HealthCheckType(CfnAWSDataType):
        def __init__(self, api_response):
            pass

        @property
        def HealthyThreshold(self):
            pass

        @property
        def Interval(self):
            pass

        @property
        def Target(self):
            pass

        @property
        def Timeout(self):
            pass

        @property
        def UnhealthyThreshold(self):
            pass

    class _LBCookieStickinessPolicy(CfnAWSDataType):
        def __init__(self, api_response):
            pass

        @property
        def CookieExpirationPeriod(self):
            pass

        @property
        def PolicyName(self):
            pass

    class _ListenerProperty(CfnAWSDataType):
        def __init__(self, api_response):
            pass

        @property
        def InstancePort(self):
            pass

        @property
        def InstanceProtocol(self):
            pass

        @property
        def LoadBalancerPort(self):
            pass

        @property
        def PolicyNames(self):
            pass

        @property
        def Protocol(self):
            pass

        @property
        def SSLCertificateId(self):
            pass

    class _Policy(CfnAWSDataType):
        def __init__(self, api_response):
            pass

        @property
        def Attributes(self):
            pass

        @property
        def InstancePorts(self):
            pass

        @property
        def LoadBalancerPorts(self):
            pass

        @property
        def PolicyName(self):
            pass

        @property
        def PolicyType(self):
            pass

    def __init__(self, api_response):
        CfnAWSResource.__init__(api_response, "AWS::ElasticLoadBalancing::LoadBalancer")

    def _cfn_id(self):
        return self._get_api_response('LoadBalancerName')

    @property
    def AppCookieStickinessPolicy(self):
        pass

    @property
    def AvailabilityZones(self):
        return self._get_api_response('AvailabilityZones')

    @property
    def HealthCheck(self):
        pass

    @property
    def Instances(self):
        return [ cfn_resourceref(i) for i in self._get_api_response('Instances') ]

    @property
    def LBCookieStickinessPoilcy(self):
        pass

    @property
    def Listeners(self):
        pass

    @property
    def Policies(self):
        pass

    @property
    def Scheme(self):
        return self._get_api_response('Scheme')

    @property
    def SecurityGroups(self):
        pass

    @property
    def Subnets(self):
        pass

