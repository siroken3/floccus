# -*- coding:utf-8 -*-

from json import JSONEncoder
import utils

class CfnJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, CfnAWSObject):
            return o._cfn_expr()
        return JSONEncoder.default(self, o)

class CfnAWSObject(object):

    def _cfn_expr(self):
        pass

class CfnAWSApiResponse(CfnAWSObject):
    def __init__(self, api_response):
        self.__api_response = api_response

    def _has_api_response(self, key):
        return self.__api_response.has_key(key)

    def _get_api_response(self, name):
        return self.__api_response[name]

    def _resource_properties(self):
        properties = {}
        entrykeys = [p for p in dir(self) if not p.startswith('_')]
        for entrykey in entrykeys:
            try:
                properties[entrykey] = getattr(self, entrykey)
            except KeyError:
                pass
        return properties

class CfnAWSResource(CfnAWSApiResponse):
    def __init__(self, api_response, resource_type):
        CfnAWSApiResponse.__init__(self, api_response)
        self._resource_type = resource_type

    def _name(self):
        return utils.normalize_name(self._cfn_id())

    def _resource_properties(self):
        properties = {}
        entrykeys = [p for p in dir(self) if not p.startswith('_')]
        for entrykey in entrykeys:
            try:
                properties[entrykey] = getattr(self, entrykey)
            except KeyError:
                pass
        return properties

    def _cfn_expr(self):
        return {
            self._name(): {
                "Type": self._resource_type,
                "Properties": self._resource_properties()
                }
            }

class CfnAWSResourceRef(CfnAWSObject):
    def __init__(self, cfn_resource):
        self.cfn_resource = cfn_resource

    def _cfn_id(self):
        return self.cfn_resource._cfn_id()

    def _cfn_expr(self):
        return { 'Ref': self.cfn_resource._name() }

class CfnTaggedResource(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, vpc)

class CfnVpc(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, 'AWS::EC2::VPC')

    def _cfn_id(self):
        return self._get_api_response('vpcId')

    @property
    def CidrBlock(self):
        return self._get_api_response('cidrBlock')

    @property
    def InstanceTenancy(self):
        return self._get_api_response('instanceTenancy')


class CfnInternetGateway(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::InternetGateway")

    def _cfn_id(self):
        return self._get_api_response('internetGatewayId')

    @property
    def Tags(self):
        return self._get_api_response('tagSet')

class CfnInternetGatewayAttachment(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc, cfn_internet_gateways):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::VPCGatewayAttachment")
        self.__vpc = CfnAWSResourceRef(cfn_vpc)
        for cfn_igw in cfn_internet_gateways:
            if self._get_api_response('internetGatewayId') == cfn_igw._cfn_id():
                self.__internet_gateway = CfnAWSResourceRef(cfn_igw)
                break

    def _cfn_id(self):
        return self.__vpc._cfn_id() + self.__internet_gateway._cfn_id()

    @property
    def InternetGatewayId(self):
        return self.__internet_gateway

    @property
    def VpcId(self):
        return self.__vpc

class CfnSubnet(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::Subnet")
        self.__vpc = CfnAWSResourceRef(cfn_vpc)

    def _cfn_id(self):
        return self._get_api_response('subnetId')

    @property
    def AvailabilityZone(self):
        return self._get_api_response('availabilityZone')

    @property
    def CidrBlock(self):
        return self._get_api_response('cidrBlock')

    @property
    def VpcId(self):
        return self.__vpc

class CfnSecurityGroupRulePropertyType(CfnAWSApiResponse):
    def _cfn_expr(self):
        return self._resource_properties()

    @property
    def IpProtocol(self):
        return self._get_api_response('ipProtocol')

    @property
    def CidrIp(self):
        return self._get_api_response('cidrIp')

    @property
    def FromPort(self):
        if self._has_api_response('fromPort'):
            return str(self._get_api_response('fromPort'))
        else:
            return "0"

    @property
    def ToPort(self):
        if self._has_api_response('toPort'):
            return str(self._get_api_response('toPort'))
        else:
            return "65536"

class CfnSecurityGroup(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::SecurityGroup")

        # vpcId
        self.__vpc = CfnAWSResourceRef(cfn_vpc)

        # ipPermissions
        ingresses = []
        for ipPermission in api_response['ipPermissions']:
            ingresses.extend(utils.flatten(ipPermission, 'ipRanges'))
        self.__ipPermissions = [CfnSecurityGroupRulePropertyType(ingress) for ingress in ingresses]

        # ipPermissionEgress
        egresses = []
        for ipPermission in api_response['ipPermissionsEgress']:
            egresses.extend(utils.flatten(ipPermission, 'ipRanges'))
        self.__ipPermissionEgress = [CfnSecurityGroupRulePropertyType(egress) for egress in egresses]

    def _cfn_id(self):
        return self.__vpc._cfn_id() + self._get_api_response('groupName') + "SecurityGroup"

    @property
    def GroupDescription(self):
        return self._get_api_response('groupDescription')

    @property
    def SecurityGroupIngress(self):
        return self.__ipPermissions

    @property
    def SecurityGroupEgress(self):
        return self.__ipPermissionEgress

    @property
    def VpcId(self):
        return self.__vpc

class CfnRouteTable(CfnTaggedResource):
    def __init__(self, api_response, cfn_vpc):
        CfnTaggedResource.__init__(self, api_response)

class CfnSubnetRouteTableAssociation(CfnAWSResource):
    def __init__(self, api_response, cfn_route_table, cfn_subnet):
        CfnAWSResource.__init__(self, api_response)

class CfnRoute(CfnAWSResource):
    def __init__(self, api_response, cfn_route_table, cfn_gateway=None, cfn_instance=None, cfn_network_interface=None):
        CfnAWSResource.__init__(self, api_response)

class CfnEC2Instance(CfnTaggedResource):
    def __init__(self, api_response, cfn_subnet):
        CfnTaggedResource.__init__(self, api_response)

class CfnAutoScalingLaunchConfiguration(CfnAWSResource):
    def __init__(self, api_response, cfn_security_groups):
        CfnAWSResource.__init__(self, api_response)

class CfnAutoScalingGroup(CfnTaggedResource):
    def __init__(self, api_response, cfn_launch_configuration, cfn_subnets):
        CfnTaggedResource.__init__(self, api_response)

class CfnNotificationConfiguration(CfnAWSResource):
    def __init__(self, api_response, cfn_auto_scaling_group, cfn_sns_topic):
        CfnAWSResource.__init__(self, api_response)

class CfnAutoScalingPolicy(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response)

class CfnSnsTopics(CfnAWSResource):
    def __init__(self, api_response, subscriptions):
        CfnAWSResource.__init__(self, api_response)

class CfnDBInstance(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response)
