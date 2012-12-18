# -*- coding:utf-8 -*-

class CfnAWSResource:
    def __init__(self, botoobj):
        self.__botoobj = botoobj

    def __getattr__(self, name):
        return getattr(self.__botoobj, name)

class CfnVpc(CfnAWSResource):
    def __init__(self, vpc):
        CfnAWSResource.__init__(self, vpc)

class CfnInternetGateWay(CfnAWSResource):
    def __init__(self, internet_gateway):
        CfnAWSResource.__init__(self, internet_gateway)

class CfnVpcGatewayAttachment(CfnAWSResource):
    def __init__(self, attachment, gateway):
        CfnAWSResource.__init__(self, attachment)
        self.gateway = gateway

class CfnSubnet(CfnAWSResource):
    def __init__(self, subnet):
        CfnAWSResource.__init__(self, subnet)

class CfnRouteTable(CfnAWSResource):
    def __init__(self, route_table):
        CfnAWSResource.__init__(self, route_table)

class CfnSubnetRouteTableAssociation(CfnAWSResource):
    def __init__(self, route_table_association):
        CfnAWSResource.__init__(self, route_table_association)

class CfnEC2Instance(CfnAWSResource):
    def __init__(self, instance):
        CfnAWSResource.__init__(self, instance)
        self._set_name_from_tag()

    def _set_name_from_tag(self):
        for key,value in self.tags.items():
            if key == 'Name':
                self.tag_name = value
                break

    def logical_id(self):
        return self.tag_name

class CfnRoute(CfnAWSResource):
    def __init__(self, route, route_table):
        CfnAWSResource.__init__(self, route)
        self.route_table = route_table
