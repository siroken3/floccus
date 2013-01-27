# -*- coding:utf-8 -*-

import os
import argparse

import botocore.session
from botocore.session import EnviromnentVariables

from models import *

class Floccus:

    def __init__(self, access_key, secret_key, region_name='us-east-1'):
        if access_key is not None:
            os.environ[EnviromnentVariables['access_key']]  = access_key
        if secret_key is not None:
            os.environ[EnviromnentVariables['secret_key']]  = secret_key
        if region_name is not None:
            os.environ[EnviromnentVariables['region_name']] = region_name
            self.region_name = region_name
        session = botocore.session.get_session()
        self.ec2service = session.get_service('ec2')
        self.endpoint = self.ec2service.get_endpoint(self.region_name)

    def form(self):
        context = {}
        vpcs = self._form_vpc(context)
        for vpc in vpcs:
            internet_gateways     = self._form_internet_gateway(context, vpc)
            subnets               = self._form_subnets(context, vpc)
            security_groups       = self._form_security_groups(context, vpc)
            instances             = self._form_instances(context, vpc, subnets)
            route_tables          = self._form_route_tables(context, vpc)
            launch_configurations = self._form_auto_scaling_launch_configuration(context, security_groups)
            self._form_gateway_attachments(context, vpc, internet_gateways)
            self._form_subnet_route_table_association(context, route_tables, subnets)
            self._form_route(context, route_tables, internet_gateways, instances)
            self._form_auto_scaling_group(context, launch_configurations, subnets)

        policies              = self._form_auto_scaling_policy(context)
        topics                = self._form_sns_topics(context)
        db_instances          = self._form_db_instance(context)
        return context

    def _form_vpc(self, context):
        operation = self.ec2service.get_operation('DescribeVpcs')
        http_response, data = operation.call(self.endpoint)
        vpcs = [CfnVpc(vpc) for vpc in data['vpcSet']]
        context['vpcs'] = vpcs
        return vpcs

    def _form_internet_gateway(self, context, vpc):
        operation = self.ec2service.get_operation('DescribeInternetGateways')
        http_response, data = operation.call(self.endpoint)
        internet_gateways = [CfnInternetGateWay(igw) for igw in data['internetGatewaySet']]
        context['internet_gateways'] = internet_gateways
        return internet_gateways

    def _form_gateway_attachments(self, context, vpc, internet_gateways):
        attachments       = []
        context['gateway_attachments'] = attachments
        return attachments

    def _form_subnets(self, context, vpc):
        subnets = []
        self._add_cfn_resource_map(context, subnets)
        context['subnets'] = subnets
        return subnets

    def _form_security_groups(self, context, vpc):
        security_groups = []
        context['security_groups'] = security_groups
        return security_groups

    def _form_route_tables(self, context, vpc):
        route_tables = []
        context['route_tables'] = route_tables
        return route_tables

    def _form_instances(self, context, vpc, subnets):
        instances = []
        context['instances'] = instances
        return instances

    def _form_route(self, context, route_tables=[], internet_gateways=[], instances=[], network_interfaces=[]):
        routes             = []
        context['routes'] = routes
        return routes

    def _form_subnet_route_table_association(self, context, route_tables, subnets):
        associations = []
        context['subnet_route_table_associations'] = associations
        return associations

    def _form_auto_scaling_launch_configuration(self, context, cfn_security_groups):
        configurations = []
        context['launch_configurations'] = configurations
        return configurations

    def _form_auto_scaling_group(self, context, launch_configurations, subnets):
        groups = []
        context['auto_scaling_groups'] = groups
        return groups

    def _form_auto_scaling_policy(self, context):
        auto_scaling_policies = []
        context['scaling_policies'] = auto_scaling_policies
        return auto_scaling_policies

    def _form_sns_topics(self, context):
        topics = []
        context['sns_topics'] = topics
        return topics

    def _form_db_instance(self, context):
        db_instances = []
        context['db_instances'] = db_instances
        return db_instances

    def _add_cfn_resource_map(self, context, cfn_objects):
        cfn_resource_map = context['cfn_resource_map'] if 'cfn_resource_map' in context else {}
        for cfn_object in cfn_objects:
            cfn_resource_map[cfn_object.id] = cfn_object.cfn_resource_name()
        context['cfn_resource_map'] = cfn_resource_map

