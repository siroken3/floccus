class CfnAWSResource:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.typestring

class CfnVpc(CfnAWSResource):
    typestring = 'AWS::EC2::VPC'

    def __init__(self, vpc):
        self.value = vpc

class CfnSubnet(CfnAWSResource):
    typestring = 'AWS::EC2::Subnet'

    def __init__(self, subnet):
        self.value = subnet

class CfnRouteTable(CfnAWSResource):
    typestring = 'AWS::EC2::RouteTable'

    def __init__(self, route_table):
        self.value = route_table

class CfnSubnetRouteTableAssociation(CfnAWSResource):
    typestring = 'AWS::EC2::SubnetRouteTableAssociation'

    def __init__(self, route_table_association):
        self.value = route_table_association

class CfnRoute(CfnAWSResource):
    typestring = 'AWS::EC2::Route'

    def __init__(self, route):
        self.value = route

