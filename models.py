class CfnAWSResource:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.typestring

class CfnVpc(CfnAWSResource):
    typestring = 'AWS::EC2::VPC'

    def __init__(self, vpc):
        self.vpc = vpc
        self.cidr_block = vpc.cidr_block
        self.instanceTenancy = vpc.instanceTenancy

    def __str__(self):
        return """
                   "MyVPC": {
                      "Type" : "%(type)s",
                      "Properties": {
                          "CidrBlock": %(cidr)s,
                          "InstanceTenancy": %(tenancy)s
                       }
                   }
               """ % {'type': self.typestring,'cidr': self.cidr_block,'tenancy':self.instanceTenancy}

class CfnSubnet(CfnAWSResource):
    typestring = 'AWS::EC2::Subnet'

    def __init__(self, subnet):
        self.subnet = subnet

    def __str__(self):
        return "hoge"
        return """
                   "MySubnet": {
                       "Type" : "%(type)s",
                       "Properties" : {
                           "AvailabilityZone" : %(zone)s,
                           "CidrBlock" : %(cidr)s,
                           "VpcId" : { "Ref" : %(vpc)s }
                       }
                   }
               """

class CfnRouteTable(CfnAWSResource):
    typestring = 'AWS::EC2::RouteTable'

    def __init__(self, route_table):
        self.route_table = route_table
        self.associations = route_table.associations


class CfnSubnetRouteTableAssociation(CfnAWSResource):
    typestring = 'AWS::EC2::SubnetRouteTableAssociation'

    def __init__(self, route_table_association):
        self.route_table_association = route_table_association
        self.route_table_id = route_table_association.route_table_id
        self.subnet_id = route_table_association.subnet_id


