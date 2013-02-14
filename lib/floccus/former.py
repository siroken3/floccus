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
        vpcs = self._form_vpc()
        for vpc in vpcs:
            stack['Resources'].update(json.loads(json.dumps(vpc, cls=CfnJsonEncoder, sort_keys=True)))
            internet_gateways     = self._form_internet_gateway(vpc)
            subnets               = self._form_subnets(vpc)
            security_groups       = self._form_security_groups(vpc)
            instances             = self._form_instances(vpc, subnets)
            route_tables          = self._form_route_tables(vpc)
            launch_configurations = self._form_auto_scaling_launch_configuration(security_groups)
            self._form_gateway_attachments(vpc, internet_gateways)
            self._form_subnet_route_table_association(route_tables, subnets)
            self._form_route(route_tables, internet_gateways, instances)
            self._form_auto_scaling_group(launch_configurations, subnets)

        policies              = self._form_auto_scaling_policy()
        topics                = self._form_sns_topics()
        db_instances          = self._form_db_instance()
        return stack

    def _form_vpc(self):
        endpoint = self.ec2service.get_endpoint('ap-northeast-1')
        operation = self.ec2service.get_operation('DescribeVpcs')
        http_response, data = operation.call(endpoint)
        vpcs = [CfnVpc(vpc) for vpc in data['vpcSet']]
        return vpcs

    def _form_internet_gateway(self, vpc):
        endpoint = self.ec2service.get_endpoint('ap-northeast-1')
        operation = self.ec2service.get_operation('DescribeInternetGateways')
        http_response, data = operation.call(endpoint)
        internet_gateways = [CfnInternetGateway(igw) for igw in data['internetGatewaySet']]
        return internet_gateways

    def _form_gateway_attachments(self, vpc, internet_gateways):
        attachments       = []
        return attachments

    def _form_subnets(self, vpc):
        subnets = []
        return subnets

    def _form_security_groups(self, vpc):
        security_groups = []
        return security_groups

    def _form_route_tables(self, vpc):
        route_tables = []
        return route_tables

    def _form_instances(self, vpc, subnets):
        instances = []
        return instances

    def _form_route(self, route_tables=[], internet_gateways=[], instances=[], network_interfaces=[]):
        routes             = []
        return routes

    def _form_subnet_route_table_association(self, route_tables, subnets):
        associations = []
        return associations

    def _form_auto_scaling_launch_configuration(self, cfn_security_groups):
        configurations = []
        return configurations

    def _form_auto_scaling_group(self, launch_configurations, subnets):
        groups = []
        return groups

    def _form_auto_scaling_policy(self):
        auto_scaling_policies = []
        return auto_scaling_policies

    def _form_sns_topics(self):
        topics = []
        return topics

    def _form_db_instance(self):
        db_instances = []
        return db_instances
