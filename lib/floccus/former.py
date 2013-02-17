# -*- coding:utf-8 -*-

import os
import argparse

import botocore.session

from floccus.models import *

class Former(object):

    def __init__(self):
        self.session = botocore.session.get_session()
        self.ec2service = self.session.get_service('ec2')

    def form(self):
        stack = {"Resources":{}}
        vpcs = self._form_vpc(stack)
        for vpc in vpcs:
            igws, gw_attachments  = self._form_internet_gateway(stack)
            subnets               = self._form_subnets(stack, vpc)
            security_groups       = self._form_security_groups(stack, vpc)
            instances             = self._form_instances(stack, vpc, subnets)
            route_tables          = self._form_route_tables(stack, vpc)
            launch_configurations = self._form_auto_scaling_launch_configuration(stack, security_groups)
            self._form_subnet_route_table_association(stack, route_tables, subnets)
            self._form_route(stack, route_tables, igws, instances)
            self._form_auto_scaling_group(stack, launch_configurations, subnets)

        policies              = self._form_auto_scaling_policy(stack)
        topics                = self._form_sns_topics(stack)
        db_instances          = self._form_db_instance(stack)
        return stack

    def _form_vpc(self, stack):
        endpoint = self.ec2service.get_endpoint('ap-northeast-1')
        operation = self.ec2service.get_operation('DescribeVpcs')
        http_response, data = operation.call(endpoint)
        vpcs = [CfnVpc(vpc) for vpc in data['vpcSet']]
        self._add_resources(stack, vpcs)
        return vpcs

    def _form_internet_gateway(self, stack):
        endpoint = self.ec2service.get_endpoint('ap-northeast-1')
        operation = self.ec2service.get_operation('DescribeInternetGateways')
        http_response, data = operation.call(endpoint)
        cfn_internet_gateways = []
        cfn_gateway_attachments = []
        for igw in data['internetGatewaySet']:
            cfn_internet_gateway = CfnInternetGateway(igw)
            cfn_internet_gateways.append(cfn_internet_gateway)
            print igw
            gateway_id = igw['internetGatewayId']
            for attachment in igw['attachmentSet']:
                cfn_gateway_attachments.append(CfnInternetGatewayAttachment(attachment, gateway_id))
        self._add_resources(stack, cfn_internet_gateways)
        self._add_resources(stack, cfn_gateway_attachments)
        return (cfn_internet_gateways, cfn_gateway_attachments)

    def _form_gateway_attachments(self, stack, internet_gateways):
        gateway_attachments = []
        self._add_resources(stack, gateway_attachments)
        return gateway_attachments

    def _form_subnets(self, stack, vpc):
        subnets = []
        self._add_resources(stack, subnets)
        return subnets

    def _form_security_groups(self, stack, vpc):
        security_groups = []
        self._add_resources(stack, security_groups)
        return security_groups

    def _form_route_tables(self, stack, vpc):
        route_tables = []
        self._add_resources(stack, route_tables)
        return route_tables

    def _form_instances(self, stack, vpc, subnets):
        instances = []
        self._add_resources(stack, instances)
        return instances

    def _form_route(self, stack, route_tables=[], internet_gateways=[], instances=[], network_interfaces=[]):
        routes             = []
        self._add_resources(stack, routes)
        return routes

    def _form_subnet_route_table_association(self, stack, route_tables, subnets):
        associations = []
        self._add_resources(stack, associations)
        return associations

    def _form_auto_scaling_launch_configuration(self, stack, cfn_security_groups):
        configurations = []
        self._add_resources(stack, configurations)
        return configurations

    def _form_auto_scaling_group(self, stack, launch_configurations, subnets):
        groups = []
        self._add_resources(stack, groups)
        return groups

    def _form_auto_scaling_policy(self, stack):
        auto_scaling_policies = []
        self._add_resources(stack, auto_scaling_policies)
        return auto_scaling_policies

    def _form_sns_topics(self, stack):
        topics = []
        return topics

    def _form_db_instance(self, stack):
        db_instances = []
        return db_instances

    def _add_resources(self, stack, resources):
        for resource in resources:
            stack['Resources'].update(resource._cfn_expr())
