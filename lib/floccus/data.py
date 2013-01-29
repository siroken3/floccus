# -*0 coding:utf-8 -*-

cfn_properties = {
    "AWS::EC2::VPC" : {
        "cidrBlock": ("CidrBlock","self.api_response[api_key]"),
        "instanceTenancy": ("InstanceTenancy","self.api_response[api_key]")
        },
    "AWS::EC2::InternetGateway" : {
        "tagSet": ("Tags","self.api_response[api_key]")
        },
    "AWS::EC2::VPCGatewayAttachment": {
        "vpc": ("VpcId","getattr(self, api_key)"),
        "internet_gateway": ("InternetGatewayId","getattr(self, api_key)")
        },
    "AWS::EC2::Subnet": {
        "availabilityZone": ("AvailabilityZone","self.api_response[api_key]"),
        "cidrBlock": ("CidrBlock","self.api_response[api_key]"),
        "vpc": ("VpcId", "getattr(self, api_key)")
        },
    "AWS::EC2::SecurityGroup": {
        "groupDescription": ("GroupDescription","self.api_response[api_key]"),
        "ipPermissions": ("SecurityGroupIngress","[p for p in getattr(self, api_key)]"),
        "ipPermissionEgress": ("SecurityGroupEgress","[p for p in getattr(self, api_key)]"),
        "vpc": ("VpcId","getattr(self, api_key)")
        }
    }
