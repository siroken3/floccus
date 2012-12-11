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
        self.vpc_filter = ('vpc-id', vpc_id)
        self.vpc_attachment_filter = ('attachment.vpc-id', vpc_id)

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
        self._form_route_tables(context)
        self._form_instances(context)
        self._form_route(context)
        self._form_subnet_route_table_association(context)
        return context

    def _form_vpc(self, context):
        vpcs = self.vpcconn.get_all_vpcs(filters=[self.vpc_filter])
        context['vpc'] = CfnVpc(vpcs[0])

    def _form_internet_gateway(self, context):
        context['internet_gateways'] = [CfnInternetGateWay(igw) for igw
                                              in self.vpcconn.get_all_internet_gateways(
                filters=[self.vpc_attachment_filter]
                )]

    def _form_gateway_attachments(self, context):
        internet_gateways = context['internet_gateways']
        attachments = []
        for internet_gateway in internet_gateways:
            attachments.extend([CfnVpcGatewayAttachment(att, internet_gateway) for att in internet_gateway.attachments])
        context['gateway_attachments'] = attachments

    def _form_subnets(self, context):
        context['subnets'] = [CfnSubnet(s) for s
                                    in self.vpcconn.get_all_subnets(
                filters=[self.vpc_filter]
                )]

    def _form_route_tables(self, context):
        context['route_tables'] = [CfnRouteTable(rtb) for rtb
                                         in self.vpcconn.get_all_route_tables(
                filters=[self.vpc_filter]
                )]

    def _form_instances(self, context):
        instances = []
        for reservation in self.vpcconn.get_all_instances(filters={'vpc-id': self.vpc_id}):
            for instance in reservation.instances:
                instances.append(CfnEC2Instance(instance))
        context['instances'] = instances

    def _form_route(self, context):
        route_tables = context['route_tables']
        routes = []
        for route_table in route_tables:
            routes.extend([CfnRoute(route, route_table) for route in route_table.routes])
        context['routes'] = routes

    def _form_subnet_route_table_association(self, context):
        route_tables = context['route_tables']
        associations = []
        for route_table in route_tables:
            associations.extend([CfnSubnetRouteTableAssociation(assoc) for assoc in route_table.associations])
        context['subnet_route_table_associations'] = associations

