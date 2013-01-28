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
        "vpc": ("VpcId","getattr(self, key).to_cfn_ref()"),
        "internet_gateway": ("InternetGatewayId","getattr(self, key).to_cfn_ref()")
        },
    "AWS::EC2::Subnet": {
        "availabilityZone": ("AvailabilityZone","self.api_response[key]"),
        "cidrBlock": ("CidrBlock","self.api_response[key]"),
        "vpc": ("VpcId", "getattr(self, key).to_cfn_ref()")
        }
    }
