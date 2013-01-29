# -*- coding:utf-8 -*-

from json import JSONEncoder
import utils
import data

class CfnJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, CfnAWSObject):
            return o.to_json()
        return JSONEncoder.default(self, o)

class CfnAWSObject(object):
    def to_json(self):
        pass

class CfnAWSResource(CfnAWSObject):
    def __init__(self, api_response):
        self.api_response = api_response

    def name(self):
        return utils.normalize_name(self.cfn_id())

    def resource_properties(self):
        properties = {}
        propertymap = data.cfn_properties[self.resource_type()]
        for api_key,cfn_property in propertymap.items():
            property_name, property_value = cfn_property
            properties[property_name] = eval(property_value)
        return properties

    def to_json(self):
        return {
            self.name(): {
                "Type": self.resource_type(),
                "Properties": self.resource_properties()
                }
            }

class CfnAWSResourceRef(CfnAWSObject):
    def __init__(self, cfn_resource):
        self.cfn_resource = cfn_resource

    def cfn_id(self):
        return self.cfn_resource.cfn_id()

    def to_cfn_ref(self):
        return { 'Ref': self.cfn_resource.name() }

class CfnTaggedResource(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, vpc)

class CfnVpc(CfnAWSResource):
    def cfn_id(self):
        return self.api_response['vpcId']

    def resource_type(self):
        return "AWS::EC2::VPC"

class CfnInternetGateway(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc):
        CfnAWSResource.__init__(self, api_response)
        self.vpc = CfnAWSResourceRef(cfn_vpc)

    def cfn_id(self):
        return self.api_response['internetGatewayId']

    def resource_type(self):
        return "AWS::EC2::InternetGateway"

class CfnInternetGatewayAttachment(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc, cfn_internet_gateways):
        CfnAWSResource.__init__(self, api_response)
        self.vpc = CfnAWSResourceRef(cfn_vpc)
        for cfn_igw in cfn_internet_gateways:
            if self.api_response['internetGatewayId'] == cfn_igw.cfn_id():
                self.internet_gateway = CfnAWSResourceRef(cfn_igw)

    def cfn_id(self):
        return self.vpc.cfn_id() + self.internet_gateway.cfn_id()

    def resource_type(self):
        return "AWS::EC2::VPCGatewayAttachment"

class CfnSubnet(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc):
        CfnAWSResource.__init__(self, api_response)
        self.vpc = CfnAWSResourceRef(cfn_vpc)

    def cfn_id(self):
        return self.api_response['subnetId']

    def resource_type(self):
        return "AWS::EC2::Subnet"

class CfnSecurityGroupRulePropertyType(CfnAWSObject):
    def __init__(self, api_response):
        self.api_response = api_response

class CfnSecurityGroup(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc):
        CfnAWSResource.__init__(self, api_response)
        self.vpc = CfnAWSResourceRef(cfn_vpc)
        for ipPermission in api_response['ipPermissions']:
            ingresses = utils.flatten(ipPermission, 'ipRanges')
            self.ipPermissions = [CfnSecurityGroupRulePropertyType(ingress) for ingress in ingresses]
        for ipPermission in api_response['ipPermissionsEgress']:
            egresses = utils.flatten(ipPermission, 'ipRanges')
            self.ipPermissionEgress = [CfnSecurityGroupRulePropertyType(egress) for egress in egresses]

    def cfn_id(self):
        return self.vpc.cfn_id() + self.api_response['groupDescription'] + "SecurityGroup"

    def resource_type(self):
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
