# -*- coding:utf-8 -*-

import boto
import boto.ec2
import boto.ec2.tag
import utils

class CfnAWSResource(object):
    def __init__(self, obj):
        self.__botoobj = obj

    def __getattr__(self, name):
        return getattr(self.__botoobj, name)

    def __repr__(self):
        return self.cfn_resource_name()

    def _identity(self):
        if 'name' in self.__botoobj.__dict__.keys():
            return (self.name)
        else:
            return (self.id)

    def cfn_resource_name(self):
        return self._identity().replace('-','')

class CfnTaggedResource(CfnAWSResource):
    def __init__(self, botoobj):
        CfnAWSResource.__init__(self, botoobj)
        self._set_name_from_tag()

    def _set_name_from_tag(self):
        self.tag_name = None
        for key, value in utils.iterateTags(self.tags):
            if key == 'Name':
                self.tag_name = value
                break

    def cfn_resource_name(self):
        if self.tag_name is None:
            return self.default_cfn_resource_name()
        else:
            return self.tag_name

    def default_cfn_resource_name(self):
        return CfnAWSResource.cfn_resource_name(self)

class CfnVpc(CfnAWSResource):
    def __init__(self, vpc):
        CfnAWSResource.__init__(self, vpc)

class CfnInternetGateWay(CfnAWSResource):
    def __init__(self, internet_gateway):
        CfnAWSResource.__init__(self, internet_gateway)

class CfnVpcGatewayAttachment(CfnAWSResource):
    def __init__(self, attachment, cfn_vpc, cfn_gateway):
        CfnAWSResource.__init__(self, attachment)
        self.vpc = cfn_vpc
        self.gateway = cfn_gateway

    def cfn_resource_name(self):
        return self.vpc.cfn_resource_name() + self.gateway.cfn_resource_name() + "GatewayAttachment"

class CfnSubnet(CfnAWSResource):
    def __init__(self, subnet, cfn_vpc):
        CfnAWSResource.__init__(self, subnet)
        self.vpc = cfn_vpc

    def cfn_resource_name(self):
        return self.vpc.cfn_resource_name() + self.cidr_block.replace('.','').replace('/','') + "Subnet"

class CfnSecurityGroup(CfnAWSResource):
    def __init__(self, security_group, cfn_vpc):
        CfnAWSResource.__init__(self, security_group)
        self.vpc = cfn_vpc

    def cfn_resource_name(self):
        return self.vpc.cfn_resource_name() + self.name.replace('-','') + "SecurityGroup"

class CfnRouteTable(CfnTaggedResource):
    def __init__(self, route_table, cfn_vpc):
        CfnTaggedResource.__init__(self, route_table)
        self.vpc = cfn_vpc

class CfnSubnetRouteTableAssociation(CfnAWSResource):
    def __init__(self, route_table_association, cfn_route_table, cfn_subnet):
        CfnAWSResource.__init__(self, route_table_association)
        self.route_table = cfn_route_table
        self.subnet = cfn_subnet

class CfnRoute(CfnAWSResource):
    def __init__(self, route, cfn_route_table, cfn_gateway=None, cfn_instance=None, cfn_network_interface=None):
        CfnAWSResource.__init__(self, route)
        self.route_table = cfn_route_table
        self.gateway = cfn_gateway
        self.instance = cfn_instance
        self.network_interface = cfn_network_interface

    def cfn_resource_name(self):
        return self.route_table.cfn_resource_name() + self.destination_cidr_block.replace('/','').replace('.','')

class CfnEC2Instance(CfnTaggedResource):
    def __init__(self, instance, cfn_subnet):
        CfnTaggedResource.__init__(self, instance)
        self.subnet = cfn_subnet

class CfnAutoScalingLaunchConfiguration(CfnAWSResource):
    def __init__(self, launch_configuration, cfn_security_groups):
        CfnAWSResource.__init__(self, launch_configuration)
        self.security_groups = cfn_security_groups

    def default_cfn_resource_name(self):
        return self.name

class CfnAutoScalingGroup(CfnTaggedResource):
    def __init__(self, auto_scaling_group, cfn_launch_configuration, cfn_subnets):
        CfnTaggedResource.__init__(self, auto_scaling_group)
        self.launch_configuration = cfn_launch_configuration
        self.subnets = cfn_subnets

    def default_cfn_resource_name(self):
        return self.name

class CfnNotificationConfiguration(CfnAWSResource):
    def __init__(self, notification_configuration, cfn_auto_scaling_group, cfn_sns_topic):
        CfnAWSResource.__init__(self, notification_configuration)
        self.auto_scaling_group = cfn_auto_scaling_group
        self.topic = cfn_sns_topic

class CfnAutoScalingPolicy(CfnAWSResource):
    def __init__(self, policy):
        CfnAWSResource.__init__(self, policy)

class CfnSnsTopics(CfnAWSResource):
    def __init__(self, topic, subscriptions):
        CfnAWSResource.__init__(self, topic)
        self.topic_arn = topic['TopicArn']

        # mapping
        cfn_subscriptions = []
        for sb in subscriptions:
            entry = dict([(k,v) for k,v in sb.items() if k == 'Endpoint' or k == 'Protocol'])
            cfn_subscriptions.append(entry)
        self.subscriptions = cfn_subscriptions

    def _identity(self):
        return self.topic_arn.rsplit(':', 1)[1] + "SnsTopic"
