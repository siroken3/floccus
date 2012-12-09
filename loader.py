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
        self.vpc_filter = ('vpc-id', vpc_id)

    def form(self):
        self.vpcconn = boto.connect_vpc(
            region=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
            )
        parse_context = {}
        self._form_vpc(parse_context)
        self._form_subnets(parse_context)
        self._form_route_tables(parse_context)
        self._form_subnet_route_table_association(parse_context)
        return parse_context

    def _form_vpc(self, parse_context):
        vpcs = self.vpcconn.get_all_vpcs(filters=[self.vpc_filter])
        parse_context['vpc'] = CfnVpc(vpcs[0])

    def _form_subnets(self, parse_context):
        parse_context['subnets'] = [CfnSubnet(s) for s
                                    in self.vpcconn.get_all_subnets(
                filters=[self.vpc_filter]
                )]

    def _form_route_tables(self, parse_context):
        parse_context['route_tables'] = [CfnRouteTable(rtb) for rtb
                                         in self.vpcconn.get_all_route_tables(
                filters=[self.vpc_filter]
                )]

    def _form_subnet_route_table_association(self, parse_context):
        route_tables = parse_context['route_tables']
        associations = []
        for route_table in route_tables:
            associations.extend([CfnSubnetRouteTableAssociation(assoc) for assoc in route_table.associations])
        parse_context['subnet_route_table_association'] = associations

if __name__ == '__main__':
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument('vpcid')
    parser.add_argument('-O','--aws-access-key')
    parser.add_argument('-W','--aws-secret-key')
    parsed = parser.parse_args()
    access_key = parsed.aws_access_key if parsed.aws_access_key is not None else os.environ.get('AWS_ACCESS_KEY')
    secret_key = parsed.aws_secret_key if parsed.aws_secret_key is not None else os.environ.get('AWS_SECRET_KEY')
    former = CloudFormer(vpc_id=parsed.vpcid, access_key=access_key, secret_key=secret_key)
    print former.form()
