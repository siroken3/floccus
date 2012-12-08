class CfnAWSResource:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.typestring

class CfnVpc(CfnAWSResource):
    typestring = 'AWS::EC2::VPC'

    def __init__(self, vpc):
        self.vpc = vpc

class CfnSubnet(CfnAWSResource):
    typestring = 'AWS::EC2::Subnet'

    def __init__(self, vpc):
        self.vpc = vpc

class CfnRouteTable(CfnAWSResource):
    typestring = 'AWS::EC2::RouteTable'

    def __init__(self, vpc):
        self.vpc = vpc


class CfnSubnetRouteTableAssociation(CfnAWSResource):
    typestring = 'AWS::EC2::SubnetRouteTableAssociation'

    def __init__(self, route_table, subnet):
        self.route_table = route_table
        self.subnet = subnet


