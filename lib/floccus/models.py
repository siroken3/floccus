# -*- coding:utf-8 -*-

class CfnAWSResource(object):
    def __init__(self, botoobj):
        self.__botoobj = botoobj

    def __getattr__(self, name):
        return getattr(self.__botoobj, name)

    def cfn_resource_name(self):
        return (self.id).replace('-','')

class CfnTaggedResource(CfnAWSResource):
    def __init__(self, botoobj):
        CfnAWSResource.__init__(self, botoobj)
        self._set_name_from_tag()

    def _set_name_from_tag(self):
        self.tag_name = None
        for key,value in self.tags.items():
            if key == 'Name':
                self.tag_name = value
                break

    def cfn_resource_name(self):
        if self.tag_name is None:
            return self.default_cfn_resource_name()
        else:
            return self.tag_name

    def default_cfn_resource_name(self):
        return None

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
        return self.vpc.cfn_resource_name() + self.gateway.cfn_resource_name() + "GateWayAttachment"

class CfnSubnet(CfnAWSResource):
    def __init__(self, subnet, cfn_vpc):
        CfnAWSResource.__init__(self, subnet)
        self.vpc = cfn_vpc

    def cfn_resource_name(self):
        return self.vpc.cfn_resource_name() + self.cidr_block.replace('.','').replace('/','') + "Subnet"

class CfnRouteTable(CfnTaggedResource):
    def __init__(self, route_table, cfn_vpc):
        CfnTaggedResource.__init__(self, route_table)
        self.vpc = cfn_vpc

    def default_cfn_resource_name(self):
        return (self.id).replace('-','')

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

    def default_cfn_resource_name(self):
        return (self.id).replace('-','')

