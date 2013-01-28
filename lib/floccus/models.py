# -*- coding:utf-8 -*-

from json import JSONEncoder
import utils
import data

class CfnJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, CfnAWSResource):
            return {
                o.name(): {
                    "Type": o.resource_type(),
                    "Properties": o.resource_properties()
                    }
                }
        return JSONEncoder.default(self, o)

class CfnAWSResource(object):
    def __init__(self, api_response):
        self.api_response = api_response

    def name(self):
        return utils.normalize_name(self.cfn_id())

    def resource_properties(self):
        properties = {}
        propertymap = data.cfn_properties[self.resource_type()]
        for key,value in propertymap.items():
            property_name, property_value = value
            properties[property_name] = eval(property_value)
        return properties

class CfnAWSResourceRef():
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

class CfnSecurityGroup(CfnAWSResource):
    def __init__(self, security_group, cfn_vpc):
        CfnAWSResource.__init__(self, security_group)

class CfnRouteTable(CfnTaggedResource):
    def __init__(self, route_table, cfn_vpc):
        CfnTaggedResource.__init__(self, route_table)

class CfnSubnetRouteTableAssociation(CfnAWSResource):
    def __init__(self, route_table_association, cfn_route_table, cfn_subnet):
        CfnAWSResource.__init__(self, route_table_association)

class CfnRoute(CfnAWSResource):
    def __init__(self, route, cfn_route_table, cfn_gateway=None, cfn_instance=None, cfn_network_interface=None):
        CfnAWSResource.__init__(self, route)

class CfnEC2Instance(CfnTaggedResource):
    def __init__(self, instance, cfn_subnet):
        CfnTaggedResource.__init__(self, instance)

class CfnAutoScalingLaunchConfiguration(CfnAWSResource):
    def __init__(self, launch_configuration, cfn_security_groups):
        CfnAWSResource.__init__(self, launch_configuration)

class CfnAutoScalingGroup(CfnTaggedResource):
    def __init__(self, auto_scaling_group, cfn_launch_configuration, cfn_subnets):
        CfnTaggedResource.__init__(self, auto_scaling_group)

class CfnNotificationConfiguration(CfnAWSResource):
    def __init__(self, notification_configuration, cfn_auto_scaling_group, cfn_sns_topic):
        CfnAWSResource.__init__(self, notification_configuration)

class CfnAutoScalingPolicy(CfnAWSResource):
    def __init__(self, policy):
        CfnAWSResource.__init__(self, policy)

class CfnSnsTopics(CfnAWSResource):
    def __init__(self, topic, subscriptions):
        CfnAWSResource.__init__(self, topic)

class CfnDBInstance(CfnAWSResource):
    def __init__(self, db_instance):
        CfnAWSResource.__init__(self, db_instance)
