# -*0 coding:utf-8 -*-

from floccus.models import *
import json

vpcs = [
CfnVpc(
        {u'cidrBlock': u'10.0.0.0/16',
         u'dhcpOptionsId': u'dopt-ae7704c7',
         u'instanceTenancy': u'default',
         u'state': u'available',
         u'vpcId': u'vpc-aa7704c3'})
]

def test_vpc():
    vpc = vpcs[0]
    expects = json.dumps({
        "vpcaa7704c3":{
            "Type":"AWS::EC2::VPC",
            "Properties": {
                "CidrBlock":"10.0.0.0/16",
                "InstanceTenancy":"default"
                }
            }
        }, sort_keys=True)
    result = json.dumps(vpc, cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_internetgateway():
    igw = CfnInternetGateWay(
        {u'attachmentSet': [{u'state': u'available', u'vpcId': u'vpc-aa7704c3'}],
         u'internetGatewayId': u'igw-a17704c8',
         u'tagSet': []}
        , vpcs[0])
    expects = json.dumps({
            "igwa17704c8": {
                "Type":"AWS::EC2::InternetGateway",
                "Properties": {
                    "Tags": []
                    }
                }
            }, sort_keys=True)
    result = json.dumps(igw, cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_subnet():
    subnet = CfnSubnet(
        {u'availabilityZone': u'ap-northeast-1a',
         u'availableIpAddressCount': 249,
         u'cidrBlock': u'10.0.3.0/24',
         u'state': u'available',
         u'subnetId': u'subnet-78760511',
         u'vpcId': u'vpc-aa7704c3'},
        vpcs[0]
        )
    expects = json.dumps({
            "subnet78760511": {
                "Type": "AWS::EC2::Subnet",
                "Properties": {
                    "AvailabilityZone" : "ap-northeast-1a",
                    "CidrBlock": "10.0.3.0/24",
                    "VpcId": { "Ref": "vpcaa7704c3" }
                    }
            }}, sort_keys=True)
    result = json.dumps(subnet, cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects
