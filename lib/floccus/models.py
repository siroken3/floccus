# -*- coding:utf-8 -*-

from json import JSONEncoder
import utils
import data

class CfnJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, CfnAWSObject):
            return o._cfn_expr()
        return JSONEncoder.default(self, o)

class CfnAWSObject(object):
    def _cfn_expr(self):
        pass

class CfnAWSResource(CfnAWSObject):
    def __init__(self, api_response):
        self.api_response = api_response

    def _name(self):
        return utils.normalize_name(self._cfn_id())

    def _resource_properties(self):
        properties = {}
        propertymap = data.cfn_properties[self._resource_type()]
        for api_key,cfn_property in propertymap.items():
            property_name, property_value = cfn_property
            properties[property_name] = eval(property_value)
        return properties

    def _cfn_expr(self):
        return {
            self._name(): {
                "Type": self._resource_type(),
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
    def _cfn_id(self):
        return self.api_response['vpcId']

    def _resource_type(self):
        return "AWS::EC2::VPC"

class CfnInternetGateway(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc):
        CfnAWSResource.__init__(self, api_response)
        self.vpc = CfnAWSResourceRef(cfn_vpc)

    def _cfn_id(self):
        return self.api_response['internetGatewayId']

    def _resource_type(self):
        return "AWS::EC2::InternetGateway"

class CfnInternetGatewayAttachment(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc, cfn_internet_gateways):
        CfnAWSResource.__init__(self, api_response)
        self.vpc = CfnAWSResourceRef(cfn_vpc)
        for cfn_igw in cfn_internet_gateways:
            if self.api_response['internetGatewayId'] == cfn_igw._cfn_id():
                self.internet_gateway = CfnAWSResourceRef(cfn_igw)

    def _cfn_id(self):
        return self.vpc._cfn_id() + self.internet_gateway._cfn_id()

    def _resource_type(self):
        return "AWS::EC2::VPCGatewayAttachment"

class CfnSubnet(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc):
        CfnAWSResource.__init__(self, api_response)
        self.vpc = CfnAWSResourceRef(cfn_vpc)

    def _cfn_id(self):
        return self.api_response['subnetId']

    def _resource_type(self):
        return "AWS::EC2::Subnet"

class CfnSecurityGroupRulePropertyType(CfnAWSObject):
    def __init__(self, api_response):
        self.__api_response = api_response

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
        return self._resource_properties()

    @property
    def IpProtocol(self):
        return self.__api_response['ipProtocol']

    @property
    def CidrIp(self):
        return self.__api_response['cidrIp']

    @property
    def FromPort(self):
        if self.__api_response.has_key('fromPort'):
            return str(self.__api_response['fromPort'])
        else:
            return "0"

    @property
    def ToPort(self):
        if self.__api_response.has_key('toPort'):
            return str(self.__api_response['toPort'])
        else:
            return "65536"

class CfnSecurityGroup(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc):
        CfnAWSResource.__init__(self, api_response)
        self.vpc = CfnAWSResourceRef(cfn_vpc)
        ingresses = []
        for ipPermission in api_response['ipPermissions']:
            ingresses.extend(utils.flatten(ipPermission, 'ipRanges'))
        self.ipPermissions = [CfnSecurityGroupRulePropertyType(ingress) for ingress in ingresses]
        egresses = []
        for ipPermission in api_response['ipPermissionsEgress']:
            egresses.extend(utils.flatten(ipPermission, 'ipRanges'))
        self.ipPermissionEgress = [CfnSecurityGroupRulePropertyType(egress) for egress in egresses]

    def _cfn_id(self):
        return self.vpc._cfn_id() + self.api_response['groupName'] + "SecurityGroup"

    def _resource_type(self):
        return "AWS::EC2::SecurityGroup"

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
