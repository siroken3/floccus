# -*- coding:utf-8 -*-

import os
import argparse
from collections import OrderedDict

import botocore.session

import floccus.utils as utils
import floccus.models as models
from floccus.models import (ec2, autoscaling, elasticloadbalancing, sns, iam, rds)

class Former(object):

    def __init__(self, region='us-east-1'):
        self.region = region
        self.session = botocore.session.get_session()
        self.ec2service = self.session.get_service('ec2')
        self.autoscaling = self.session.get_service('autoscaling')
        self.elb = self.session.get_service('elb')
        self.sns = self.session.get_service('sns')
        self.iam = self.session.get_service('iam')

    def form(self):
        stack = {"Resources":[]}
        self._form_vpc(stack)
        self._form_internet_gateway(stack)
        self._form_eip(stack)
        self._form_subnets(stack)
        self._form_security_groups(stack)
        self._form_instances(stack)
        self._form_elb(stack)
        self._form_volume(stack)
        self._form_route_tables(stack)
        self._form_network_interface(stack)
        self._form_auto_scaling_group(stack)
        self._form_auto_scaling_launch_configuration(stack)
        self._form_auto_scaling_policy(stack)
        self._form_sns(stack)
        self._form_iam(stack)
#        db_instances          = self._form_db_instance(stack)

        stack['Resources'] = OrderedDict(utils.sort_by_cfn_resource_type(stack['Resources']))
        return stack

    def _form_vpc(self, stack):
        endpoint = self.ec2service.get_endpoint(self.region)
        operation = self.ec2service.get_operation('DescribeVpcs')
        code, data = operation.call(endpoint)
        vpcs = [ec2.CfnVpc(vpc) for vpc in data['vpcSet']]
        self._add_resources(stack, vpcs)
        return vpcs

    def _form_internet_gateway(self, stack):
        endpoint = self.ec2service.get_endpoint(self.region)
        operation = self.ec2service.get_operation('DescribeInternetGateways')
        code, data = operation.call(endpoint)
        cfn_internet_gateways = []
        cfn_gateway_attachments = []
        for igw in data['internetGatewaySet']:
            cfn_internet_gateway = ec2.CfnInternetGateway(igw)
            cfn_internet_gateways.append(cfn_internet_gateway)
            gateway_id = igw['internetGatewayId']
            for attachment in igw['attachmentSet']:
                cfn_gateway_attachments.append(ec2.CfnInternetGatewayAttachment(attachment, gateway_id))
        self._add_resources(stack, cfn_internet_gateways)
        self._add_resources(stack, cfn_gateway_attachments)

    def _form_eip(self, stack):
        eips = []
        ep = self.ec2service.get_endpoint(self.region)
        op = self.ec2service.get_operation('DescribeAddresses')
        code, data = op.call(ep)
        for eip_data in data['addressesSet']:
            eips.append(ec2.CfnEC2EIP(eip_data))
        self._add_resources(stack, eips)

    def _form_subnets(self, stack):
        subnets = []
        ep = self.ec2service.get_endpoint(self.region)
        op = self.ec2service.get_operation('DescribeSubnets')
        code, data = op.call(ep)
        for subnet_data in data['subnetSet']:
            subnets.append(ec2.CfnEC2Subnet(subnet_data))
        self._add_resources(stack, subnets)

    def _form_security_groups(self, stack):
        security_groups = []
        ep = self.ec2service.get_endpoint(self.region)
        op = self.ec2service.get_operation('DescribeSecurityGroups')
        code, data = op.call(ep)
        for security_group_data in data['securityGroupInfo']:
            cfn_security_group = ec2.CfnEC2SecurityGroup(security_group_data)
            security_groups.append(cfn_security_group)
        self._add_resources(stack, security_groups)

    def _form_route_tables(self, stack):
        ep = self.ec2service.get_endpoint(self.region)
        op = self.ec2service.get_operation('DescribeRouteTables')
        code, data = op.call(ep)
        route_tables = []
        subnet_route_table_association = []
        routes = []
        for route_table_data in data['routeTableSet']:
            cfn_route_table = ec2.CfnEC2RouteTable(route_table_data)
            route_tables.append(cfn_route_table)
            route_table_id = route_table_data['routeTableId']
            for route_data in route_table_data['routeSet']:
                if route_data['origin'] == 'CreateRoute':
                    cfn_route = ec2.CfnEC2Route(route_data, route_table_id)
                    routes.append(cfn_route)
            for association_data in route_table_data['associationSet']:
                if 'subnetId' in association_data.keys():
                    cfn_route_table_association = ec2.CfnSubnetRouteTableAssociation(association_data, route_table_id)
                    subnet_route_table_association.append(cfn_route_table_association)
        self._add_resources(stack, route_tables)
        self._add_resources(stack, routes)
        self._add_resources(stack, subnet_route_table_association)

    def _form_network_interface(self, stack):
        network_interfaces = []
        ep = self.ec2service.get_endpoint(self.region)
        op = self.ec2service.get_operation('DescribeNetworkInterfaces')
        code, data = op.call(ep)
        for network_interface_data in data['networkInterfaceSet']:
            network_interfaces.append(ec2.CfnEC2NetworkInterface(network_interface_data))
        self._add_resources(stack, network_interfaces)

    def _form_instances(self, stack):
        ep = self.ec2service.get_endpoint(self.region)
        op = self.ec2service.get_operation('DescribeInstances')
        code, data = op.call(ep)
        instances = []
        for reservation in data['reservationSet']:
            for instance_data in reservation['instancesSet']:
                instances.append(ec2.CfnEC2Instance(instance_data))
        self._add_resources(stack, instances)

    def _form_elb(self, stack):
        ep = self.elb.get_endpoint(self.region)
        op = self.elb.get_operation('DescribeLoadBalancers')
        code, data = op.call(ep)
        elbs = []
        for elb in data['LoadBalancerDescriptions']:
            elbs.append(elasticloadbalancing.CfnElasticLoadBalancingLoadBalancer(elb))
        self._add_resources(stack, elbs)

    def _form_volume(self, stack):
        ep = self.ec2service.get_endpoint(self.region)
        op = self.ec2service.get_operation('DescribeVolumes')
        code, data = op.call(ep)
        volumes = []
        volume_attachments = []
        for volume_data in data['volumeSet']:
            volumes.append(ec2.CfnEC2Volume(volume_data))
            volume_id = volume_data['volumeId']
            for attachment_data in volume_data['attachmentSet']:
                volume_attachments.append(ec2.CfnEC2VolumeAttachment(attachment_data, volume_id))
        self._add_resources(stack, volumes)
        self._add_resources(stack, volume_attachments)

    def _form_auto_scaling_group(self, stack):
        ep = self.autoscaling.get_endpoint(self.region)
        op = self.autoscaling.get_operation('DescribeAutoScalingGroups')
        code, group_data = op.call(ep)
        op = self.autoscaling.get_operation('DescribeNotificationConfigurations')
        code, config_data = op.call(ep)
        groups = []
        for g_data in group_data['AutoScalingGroups']:
            groups.append(autoscaling.CfnAutoScalingAutoScalingGroup(g_data, config_data['NotificationConfigurations']))
        self._add_resources(stack, groups)

    def _form_auto_scaling_launch_configuration(self, stack):
        configurations = []
        ep = self.autoscaling.get_endpoint(self.region)
        op = self.autoscaling.get_operation('DescribeLaunchConfigurations')
        code, data = op.call(ep)
        launch_configs = []
        for launch_config_data in data['LaunchConfigurations']:
            configurations.append(autoscaling.CfnAutoScalingLaunchConfiguration(launch_config_data))
        self._add_resources(stack, configurations)

    def _form_auto_scaling_policy(self, stack):
        ep = self.autoscaling.get_endpoint(self.region)
        op = self.autoscaling.get_operation('DescribePolicies')
        code, data = op.call(ep)
        auto_scaling_policies = []
        for policy_data in data['ScalingPolicies']:
            auto_scaling_policies.append(autoscaling.CfnAutoScalingPolicy(policy_data))
        self._add_resources(stack, auto_scaling_policies)

    def _form_sns(self, stack):
        ep = self.sns.get_endpoint(self.region)
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
            topics.append(sns.CfnSNSTopic(api_response))
        self._add_resources(stack, topics)

    def _form_iam(self, stack):
        ep = self.iam.get_endpoint('us-east-1')
        op = self.iam.get_operation('ListRoles')
        code, data = op.call(ep)
        roles = []
        policies = []
        profiles = []
        role_policy_data_map = {}
        role_profiles_data_map = {}

        # Create roles
        for role_data in data['Roles']:
            roles.append(iam.CfnIAMRole(role_data))
            role_name = role_data['RoleName']

            # Create profiles
            list_instance_profiles_for_role_op = self.iam.get_operation('ListInstanceProfilesForRole')
            code, instance_profile_data = list_instance_profiles_for_role_op.call(ep, role_name=role_name)
            for instance_profile in instance_profile_data['InstanceProfiles']:
                profiles.append(iam.CfnIAMInstanceProfile(instance_profile))

            # Create policy -> roles data mapping
            list_role_policies_op = self.iam.get_operation('ListRolePolicies')
            code, policy_name_data = list_role_policies_op.call(ep, role_name=role_name)
            for policy_name in policy_name_data['PolicyNames']:
                if policy_name not in role_policy_data_map:
                    role_policy_data_map[policy_name] = []
                role_policy_data_map[policy_name].append(role_name)


        for policy_name, role_names in role_policy_data_map.items():
            op = self.iam.get_operation('GetRolePolicy')
            for role_name in role_names:
                code, role_policy = op.call(ep, role_name=role_name, policy_name=policy_name)
                role_policy['Roles'] = role_names
                policies.append(iam.CfnIAMPolicy(role_policy))

        self._add_resources(stack, roles)
        self._add_resources(stack, policies)
        self._add_resources(stack, profiles)

    def _form_db_instance(self, stack):
        db_instances = []
        self._add_resources(stack, db_instances)

    def _add_resources(self, stack, resources):
        for resource in resources:
            expr = resource._cfn_expr()
            if expr is not None:
                stack['Resources'].append(expr)
