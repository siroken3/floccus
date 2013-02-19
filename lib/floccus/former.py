# -*- coding:utf-8 -*-

import os
import argparse

import botocore.session

from floccus.models import *

class Former(object):

    def __init__(self):
        self.session = botocore.session.get_session()
        self.ec2service = self.session.get_service('ec2')
        self.autoscaling = self.session.get_service('autoscaling')
        self.sns = self.session.get_service('sns')

    def form(self):
        stack = {"Resources":{}}
        self._form_vpc(stack)
        self._form_internet_gateway(stack)
        self._form_subnets(stack)
        self._form_security_groups(stack)
        self._form_instances(stack)
        self._form_volume(stack)
        self._form_route_tables(stack)
        self._form_network_interface(stack)
        self._form_auto_scaling_group(stack)
        self._form_auto_scaling_launch_configuration(stack)
        self._form_auto_scaling_policy(stack)
        self._form_sns_topics(stack)
#        db_instances          = self._form_db_instance(stack)
        return stack

    def _form_vpc(self, stack):
        endpoint = self.ec2service.get_endpoint('ap-northeast-1')
        operation = self.ec2service.get_operation('DescribeVpcs')
        code, data = operation.call(endpoint)
        vpcs = [CfnVpc(vpc) for vpc in data['vpcSet']]
        self._add_resources(stack, vpcs)
        return vpcs

    def _form_internet_gateway(self, stack):
        endpoint = self.ec2service.get_endpoint('ap-northeast-1')
        operation = self.ec2service.get_operation('DescribeInternetGateways')
        code, data = operation.call(endpoint)
        cfn_internet_gateways = []
        cfn_gateway_attachments = []
        for igw in data['internetGatewaySet']:
            cfn_internet_gateway = CfnInternetGateway(igw)
            cfn_internet_gateways.append(cfn_internet_gateway)
            gateway_id = igw['internetGatewayId']
            for attachment in igw['attachmentSet']:
                cfn_gateway_attachments.append(CfnInternetGatewayAttachment(attachment, gateway_id))
        self._add_resources(stack, cfn_internet_gateways)
        self._add_resources(stack, cfn_gateway_attachments)

    def _form_subnets(self, stack):
        subnets = []
        ep = self.ec2service.get_endpoint('ap-northeast-1')
        op = self.ec2service.get_operation('DescribeSubnets')
        code, data = op.call(ep)
        for subnet_data in data['subnetSet']:
            cfn_subnet = CfnEC2Subnet(subnet_data)
            subnets.append(cfn_subnet)
        self._add_resources(stack, subnets)

    def _form_security_groups(self, stack):
        security_groups = []
        ep = self.ec2service.get_endpoint('ap-northeast-1')
        op = self.ec2service.get_operation('DescribeSecurityGroups')
        code, data = op.call(ep)
        for security_group_data in data['securityGroupInfo']:
            cfn_security_group = CfnEC2SecurityGroup(security_group_data)
            security_groups.append(cfn_security_group)
        self._add_resources(stack, security_groups)

    def _form_route_tables(self, stack):
        ep = self.ec2service.get_endpoint('ap-northeast-1')
        op = self.ec2service.get_operation('DescribeRouteTables')
        code, data = op.call(ep)
        route_tables = []
        subnet_route_table_association = []
        routes = []
        for route_table_data in data['routeTableSet']:
            cfn_route_table = CfnEC2RouteTable(route_table_data)
            route_tables.append(cfn_route_table)
            route_table_id = route_table_data['routeTableId']
            for route_data in route_table_data['routeSet']:
                cfn_route = CfnEC2Route(route_data, route_table_id)
                routes.append(cfn_route)
            for association_data in route_table_data['associationSet']:
                cfn_route_table_association = CfnSubnetRouteTableAssociation(association_data, route_table_id)
                subnet_route_table_association.append(cfn_route_table_association)
        self._add_resources(stack, route_tables)
        self._add_resources(stack, routes)
        self._add_resources(stack, subnet_route_table_association)

    def _form_network_interface(self, stack):
        network_interfaces = []
        ep = self.ec2service.get_endpoint('ap-northeast-1')
        op = self.ec2service.get_operation('DescribeNetworkInterfaces')
        code, data = op.call(ep)
        for network_interface_data in data['networkInterfaceSet']:
            network_interfaces.append(CfnEC2NetworkInterface(network_interface_data))
        self._add_resources(stack, network_interfaces)

    def _form_instances(self, stack):
        ep = self.ec2service.get_endpoint('ap-northeast-1')
        op = self.ec2service.get_operation('DescribeInstances')
        code, data = op.call(ep)
        instances = []
        for reservation in data['reservationSet']:
            for instance_data in reservation['instancesSet']:
                instances.append(CfnEC2Instance(instance_data))
        self._add_resources(stack, instances)

    def _form_volume(self, stack):
        ep = self.ec2service.get_endpoint('ap-northeast-1')
        op = self.ec2service.get_operation('DescribeVolumes')
        code, data = op.call(ep)
        volumes = []
        volume_attachments = []
        for volume_data in data['volumeSet']:
            volumes.append(CfnEC2Volume(volume_data))
            volume_id = volume_data['volumeId']
            for attachment_data in volume_data['attachmentSet']:
                volume_attachments.append(CfnEC2VolumeAttachment(attachment_data, volume_id))
        self._add_resources(stack, volumes)
        self._add_resources(stack, volume_attachments)

    def _form_auto_scaling_group(self, stack):
        ep = self.autoscaling.get_endpoint('ap-northeast-1')
        op = self.autoscaling.get_operation('DescribeAutoScalingGroups')
        code, group_data = op.call(ep)
        op = self.autoscaling.get_operation('DescribeNotificationConfigurations')
        code, config_data = op.call(ep)
        groups = []
        for g_data in group_data['AutoScalingGroups']:
            groups.append(CfnAutoScalingAutoScalingGroup(g_data, config_data['NotificationConfigurations']))
        self._add_resources(stack, groups)

    def _form_auto_scaling_launch_configuration(self, stack):
        configurations = []
        ep = self.autoscaling.get_endpoint('ap-northeast-1')
        op = self.autoscaling.get_operation('DescribeLaunchConfigurations')
        code, data = op.call(ep)
        launch_configs = []
        for launch_config_data in data['LaunchConfigurations']:
            configurations.append(CfnAutoScalingLaunchConfiguration(launch_config_data))
        self._add_resources(stack, configurations)

    def _form_auto_scaling_policy(self, stack):
        ep = self.autoscaling.get_endpoint('ap-northeast-1')
        op = self.autoscaling.get_operation('DescribePolicies')
        code, data = op.call(ep)
        auto_scaling_policies = []
        for policy_data in data['ScalingPolicies']:
            auto_scaling_policies.append(CfnAutoScalingPolicy(policy_data))
        self._add_resources(stack, auto_scaling_policies)

    def _form_sns_topics(self, stack):
        ep = self.sns.get_endpoint('ap-northeast-1')
        op = self.sns.get_operation('ListTopics')
        code, topic_data = op.call(ep)
        op = self.sns.get_operation('ListSubscriptions')
        code, subscription_data = op.call(ep)
        topics = []
        for td in topic_data['Topics']:
            topic_arn = td['TopicArn']
            op = self.sns.get_operation('GetTopicAttributes')
            code, t_attr = op.call(ep, topic_arn=topic_arn)
            topic_attr_data = t_attr['Attributes']
            api_response = {
                "TopicArn": topic_arn,
                "DisplayName": topic_attr_data['DisplayName'] if 'DisplayName' in topic_attr_data else "",
                "Subscriptions": [sb for sb in subscription_data['Subscriptions'] if sb['TopicArn'] == topic_arn]
            }
            topics.append(CfnSNSTopic(api_response))
        self._add_resources(stack, topics)

    def _form_db_instance(self, stack):
        db_instances = []
        self._add_resources(stack, db_instances)

    def _add_resources(self, stack, resources):
        for resource in resources:
            stack['Resources'].update(resource._cfn_expr())
