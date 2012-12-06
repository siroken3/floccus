# -*- coding:utf-8 -*-

import boto
import boto.ec2
import boto.vpc

from models import *

class CloudParser:
    def __init__(self, region_name, vpc_id):
        self.region_name = region_name
        self.vpc_filter = ('vpc-id', vpc_id)

    def walk(self):
        self.region = boto.ec2.get_region(self.region_name)
        self.vpcconn = boto.connect_vpc(region=self.region)
        parse_context = {}
        self._walk_vpc(parse_context)
        self._walk_subnets(parse_context)
        self._walk_route_tables(parse_context)
        return parse_context

    def _walk_vpc(self, parse_context):
        parse_context['vpc'] = CfnVpc(self.vpcconn.get_all_vpcs(filters=[self.vpc_filter])[0])

    def _walk_subnets(self, parse_context):
        parse_context['subnets'] = [CfnSubnet(s) for s in self.vpcconn.get_all_subnets(filters=[self.vpc_filter])]

    def _walk_route_table(self, parse_context):
        rtbs = [CfnRouteTable(rtb) for rtb in self.vpcconn.get_all_route_tables(filters=[self.vpc_filter])]
        parse_context['route_tables'] = rtbs
        assocs = [rtb.associations for rtb in rtbs]
        parse_context['subnet_route_table_associations'] = [CfnSubnetRouteTableAssociation(x) for x in assocs]

if __name__ == '__main__':
    import sys
    parser = CloudParser(sys.argv[0], sys.argv[1])
    print parser.walk()
