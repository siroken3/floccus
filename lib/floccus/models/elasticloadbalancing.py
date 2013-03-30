# -*- coding:utf-8 -*-

from floccus.models import CfnAWSResource, CfnAWSDataType, cfn_resourceref

class CfnElasticLoadBalancingLoadBalancer(CfnAWSResource):
    class _AppCookieStickinessPolicy(CfnAWSDataType):
        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)

        @property
        def CookieName(self):
            return self._get_api_response('CookieName')

        @property
        def PolicyName(self):
            return self._get_api_response('PolicyName')

    class _HealthCheckType(CfnAWSDataType):
        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)

        @property
        def HealthyThreshold(self):
            return str(self._get_api_response('HealthyThreshold'))

        @property
        def Interval(self):
            return str(self._get_api_response('Interval'))

        @property
        def Target(self):
            return self._get_api_response('Target')

        @property
        def Timeout(self):
            return str(self._get_api_response('Timeout'))

        @property
        def UnhealthyThreshold(self):
            return str(self._get_api_response('UnhealthyThreshold'))

    class _LBCookieStickinessPolicy(CfnAWSDataType):
        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)

        @property
        def CookieExpirationPeriod(self):
            return self._get_api_response('CookieExpirationPeriod')

        @property
        def PolicyName(self):
            return self._get_api_response('PolicyName')

    class _ListenerProperty(CfnAWSDataType):
        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)

        @property
        def InstancePort(self):
            return str(self._get_api_response('Listener')['InstancePort'])

        @property
        def InstanceProtocol(self):
            return self._get_api_response('Listener')['InstanceProtocol']

        @property
        def LoadBalancerPort(self):
            return str(self._get_api_response('Listener')['LoadBalancerPort'])

        @property
        def PolicyNames(self):
            return self._get_api_response('PolicyNames')

        @property
        def Protocol(self):
            return self._get_api_response('Listener')['Protocol']

        @property
        def SSLCertificateId(self):
            pass

    class _Policy(CfnAWSDataType):
        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)

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
        CfnAWSResource.__init__(self, api_response, "AWS::ElasticLoadBalancing::LoadBalancer")

    def _cfn_id(self):
        return self._get_api_response('LoadBalancerName')

    @property
    def AppCookieStickinessPolicy(self):
        policies = self._get_api_response('Policies')
        return [self._AppCookieStickinessPolicy(p)._cfn_expr() for p in policies['AppCookieStickinessPolicies']]

    @property
    def AvailabilityZones(self):
        if self._get_api_response('VPCId'):
            pass
        else:
            return self._get_api_response('AvailabilityZones')

    @property
    def HealthCheck(self):
        return self._HealthCheckType(self._get_api_response('HealthCheck'))._cfn_expr()

    @property
    def Instances(self):
        return [ cfn_resourceref(i) for i in self._get_api_response('Instances') ]

    @property
    def LBCookieStickinessPolicy(self):
        policies = self._get_api_response('Policies')
        return [self._AppCookieStickinessPolicy(p)._cfn_expr() for p in policies['LBCookieStickinessPolicies']]

    @property
    def Listeners(self):
        listeners = self._get_api_response('ListenerDescriptions')
        return [self._ListenerProperty(l)._cfn_expr() for l in listeners]

    @property
    def Policies(self):
        policies = self._get_api_response('Policies')
        return [self._Policy(p)._cfn_expr() for p in policies['OtherPolicies']]

    @property
    def Scheme(self):
        return self._get_api_response('Scheme')

    @property
    def SecurityGroups(self):
        return [cfn_resourceref(sg) for sg in self._get_api_response('SecurityGroups')]

    @property
    def Subnets(self):
        if self._get_api_response('VPCId'):
            return [cfn_resourceref(s) for s in self._get_api_response('Subnets')]
        else:
            pass
