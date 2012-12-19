# -*- coding:utf-8 -*-

import boto
import boto.ec2
import boto.vpc
import argparse

from models import *

class CloudFormer:
    def __init__(self, access_key, secret_key, vpc_id, region_name='us-east-1'):
        self.access_key = access_key if access_key is not None else ''
        self.secret_key = secret_key if secret_key is not None else ''
        self.region = boto.ec2.get_region(
            region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
            )
        self.vpc_id = vpc_id

    def form(self):
        self.vpcconn = boto.connect_vpc(
            region=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
            )
        context = {}
        self._form_vpc(context)
        self._form_internet_gateway(context)
        self._form_gateway_attachments(context)
        self._form_subnets(context)
        self._form_instances(context)
        self._form_route_tables(context)
        self._form_route(context)
        self._form_subnet_route_table_association(context)
        return context

    def _form_vpc(self, context):
        vpcs = self.vpcconn.get_all_vpcs(
            filters=[('vpc-id', self.vpc_id)]
            )
        context['vpc'] = CfnVpc(vpcs[0])

    def _form_internet_gateway(self, context):
        context['internet_gateways'] = [
            CfnInternetGateWay(igw)
            for igw in self.vpcconn.get_all_internet_gateways(
                filters=[('attachment.vpc-id',self.vpc_id)]
                )
            ]

    def _form_gateway_attachments(self, context):
        vpc               = context['vpc']
        internet_gateways = context['internet_gateways'] if 'internet_gateways' in context else []
        attachments       = []
        for internet_gateway in internet_gateways:
            attachments.extend([
                    CfnVpcGatewayAttachment(att, cfn_vpc=vpc, cfn_gateway=internet_gateway)
                    for att in internet_gateway.attachments
                    ])
        context['gateway_attachments'] = attachments

    def _form_subnets(self, context):
        vpc                = context['vpc']
        context['subnets'] = [
            CfnSubnet(s, vpc)
            for s in self.vpcconn.get_all_subnets(
                filters=[('vpc-id', vpc.id)]
                )
            ]

    def _form_route_tables(self, context):
        vpc                     = context['vpc']
        context['route_tables'] = [
            CfnRouteTable(rtb, cfn_vpc=vpc)
            for rtb in self.vpcconn.get_all_route_tables(
                filters=[('vpc-id', vpc.id)]
                )
            ]

    def _form_instances(self, context):
        vpc       = context['vpc']
        subnets   = context['subnets'] if 'subnets' in context else []
        instances = []
        for reservation in self.vpcconn.get_all_instances(filters={'vpc-id': vpc.id}):
            for instance in reservation.instances:
                    instances.extend([
                            CfnEC2Instance(instance, cfn_subnet=subnet)
                            for subnet in subnets
                            if subnet.id == instance.subnet_id
                        ])
        context['instances'] = instances

    def _form_route(self, context):
        route_tables       = context['route_tables'] if 'route_tables' in context else []
        gateways           = context['internet_gateways'] if 'internet_gateways' in context else []
        instances          = context['instances'] if 'instances' in context else []
        network_interfaces = context['network_interfaces'] if 'network_interfaces' in context else []
        routes             = []
        for route_table in route_tables:
            for gateway in gateways:
                routes.extend([
                        CfnRoute(route, cfn_route_table=route_table, cfn_gateway=gateway)
                        for route in route_table.routes
                        if gateway.id == route.gateway_id
                     ])
            for instance in instances:
                routes.extend([
                        CfnRoute(route, cfn_route_table=route_table, cfn_instance=instance)
                        for route in route_table.routes
                        if instance.id == route.instance_id
                        ])
            for network_interface in network_interfaces:
                routes.extend([
                        CfnRoute(route, cfn_route_table=route_table, cfn_network_interface=network_interface)
                        for route in route_table.routes
                        if network_interfaces.id == route.network_interface_id
                        ])
        context['routes'] = routes

    def _form_subnet_route_table_association(self, context):
        route_tables = context['route_tables']
        subnets      = context['subnets']
        associations = []
        for subnet in subnets:
            for route_table in route_tables:
                associations.extend([
                        CfnSubnetRouteTableAssociation(assoc, cfn_route_table=route_table, cfn_subnet=subnet)
                        for assoc in route_table.associations
                        if assoc.subnet_id == subnet.id
                        ])
        context['subnet_route_table_associations'] = associations

