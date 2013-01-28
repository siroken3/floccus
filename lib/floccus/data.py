# -*0 coding:utf-8 -*-

cfn_properties = {
    "AWS::EC2::VPC" : {
        "cidrBlock": ("CidrBlock","self.api_response[key]"),
        "instanceTenancy": ("InstanceTenancy","self.api_response[key]")
        },
    "AWS::EC2::InternetGateway" : {
        "tagSet": ("Tags","self.api_response[key]")
        },
    "AWS::EC2::VPCGatewayAttachment": {
        "vpcId": ("VpcId","self.api_response[key]"),
        "internetGatewayId": ("InternetGatewayId","self.api_response[key]")
        },
    "AWS::EC2::Subnet": {
        "availabilityZone": ("AvailabilityZone","self.api_response[key]"),
        "cidrBlock": ("CidrBlock","self.api_response[key]"),
        "vpcId": ("VpcId", "{'Ref': self.cfn_vpc.name()}")
        }
    }
