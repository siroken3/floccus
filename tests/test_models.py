# -*- coding:utf-8 -*-

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
internet_gateways = [CfnInternetGateway(
        {u'attachmentSet': [{u'state': u'available', u'vpcId': u'vpc-aa7704c3'}],
         u'internetGatewayId': u'igw-a17704c8',
         u'tagSet': []})
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
    igw = internet_gateways[0]
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

def test_vpcattachment_internetgateway():
    vpc = vpcs[0]
    igwattachment = CfnInternetGatewayAttachment(
        {u'attachmentSet': [{u'state': u'available',
                             u'vpcId': u'vpc-aa7704c3'}],
         u'internetGatewayId': u'igw-a17704c8',
         u'tagSet': []}, vpc, internet_gateways)
    expects = json.dumps({
            "vpcaa7704c3igwa17704c8": {
                "Type": "AWS::EC2::VPCGatewayAttachment",
                "Properties": {
                    "VpcId": { "Ref" : "vpcaa7704c3" },
                    "InternetGatewayId" : { "Ref" : "igwa17704c8" }
                    }
                }
            }, sort_keys=True)
    result = json.dumps(igwattachment, cls=CfnJsonEncoder, sort_keys=True)
    print "expects = " + expects
    print "result  = " + result
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
                }
            }, sort_keys=True)
    result = json.dumps(subnet, cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_security_group_rule_1():
    group_rule = CfnSecurityGroupRulePropertyType({
            u'fromPort': 80,
            u'groups': [],
            u'ipProtocol': u'tcp',
            u'cidrIp': u'0.0.0.0/0',
            u'toPort': 80})
    expects = json.dumps({
            "IpProtocol" : "tcp",
            "CidrIp" : "0.0.0.0/0",
            "FromPort" : "80",
            "ToPort" : "80"
            }, sort_keys=True)
    result = json.dumps(group_rule, cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_security_group_rule_2():
    group_rule = CfnSecurityGroupRulePropertyType({
            u'fromPort': 80,
            u'groups': [],
            u'ipProtocol': u'tcp',
            u'cidrIp': u'0.0.0.0/0',
            u'toPort': 80})
    expects = json.dumps({
            "IpProtocol" : "tcp",
            "CidrIp" : "0.0.0.0/0",
            "FromPort" : "80",
            "ToPort" : "80"
            }, sort_keys=True)
    result = json.dumps(group_rule, cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_security_group():
    security_group = CfnSecurityGroup(
        {'groupDescription': 'External security group',
         'groupId': 'sg-28e8f444',
         'groupName': 'external-sg',
         'ipPermissions': [{'fromPort': 22,
                             'groups': [],
                             'ipProtocol': 'tcp',
                             'ipRanges': [{'cidrIp': '210.128.90.161/32'},
                                           {'cidrIp': '221.186.108.105/32'}],
                             'toPort': 22},
                            {'fromPort': 80,
                             'groups': [],
                             'ipProtocol': 'tcp',
                             'ipRanges': [{'cidrIp': '0.0.0.0/0'}],
                             'toPort': 80},
                            {'fromPort': 8443,
                             'groups': [],
                             'ipProtocol': 'tcp',
                             'ipRanges': [{'cidrIp': '210.128.90.161/32'},
                                           {'cidrIp': '221.186.108.105/32'}],
                             'toPort': 8443}],
         'ipPermissionsEgress': [{'groups': [],
                                   'ipProtocol': '-1',
                                   'ipRanges': [{'cidrIp': '0.0.0.0/0'}]}],
         'ownerId': '478468994184',
         'vpcId': 'vpc-aa7704c3'},
        vpcs[0]
        )
    expects = json.dumps({
        "vpcaa7704c3externalsgSecurityGroup" : {
            "Type" : "AWS::EC2::SecurityGroup",
            "Properties" : {
                "GroupDescription" : "External security group",
                "SecurityGroupIngress" : [{
                        "IpProtocol" : "tcp",
                        "CidrIp" : "210.128.90.161/32",
                        "FromPort" : "22",
                        "ToPort" : "22"
                        },{
                        "IpProtocol" : "tcp",
                        "CidrIp" : "221.186.108.105/32",
                        "FromPort" : "22",
                        "ToPort" : "22"
                        },{
                        "IpProtocol" : "tcp",
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : "80",
                        "ToPort" : "80"
                        },{
                        "IpProtocol" : "tcp",
                        "CidrIp" : "210.128.90.161/32",
                        "FromPort" : "8443",
                        "ToPort" : "8443"
                        },{
                        "IpProtocol" : "tcp",
                        "CidrIp" : "221.186.108.105/32",
                        "FromPort" : "8443",
                        "ToPort" : "8443"
                        }],
                "SecurityGroupEgress" : [{
                        "IpProtocol" : "-1",
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : "0",
                        "ToPort" : "65536"
                        }],
                "VpcId" : { "Ref" : "vpcaa7704c3" }
                }
            }}, sort_keys=True)
    result = json.dumps(security_group, cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_instance():
    instance = CfnEC2Instance({})
    expects = json.dumps({},sort_keys=True)
    result = json.dumps(instance, cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_route_table():
    route_table = CfnRouteTable(
        {u'associationSet': [{u'main': True,
                              u'routeTableAssociationId': u'rtbassoc-af7704c6',
                              u'routeTableId': u'rtb-ac7704c5'}],
         u'routeSet': [{u'destinationCidrBlock': u'192.168.3.110/32',
                        u'networkInterfaceId': u'eni-bf8bf0d6',
                        u'state': u'blackhole'},
                       {u'destinationCidrBlock': u'192.168.5.100/32',
                        u'instanceId': u'i-e80c68eb',
                        u'instanceOwnerId': u'478468994184',
                        u'networkInterfaceId': u'eni-e02c6a89',
                        u'state': u'active'},
                       {u'destinationCidrBlock': u'192.168.3.100/32',
                        u'instanceId': u'i-36711635',
                        u'instanceOwnerId': u'478468994184',
                        u'networkInterfaceId': u'eni-ead89e83',
                        u'state': u'active'},
                       {u'destinationCidrBlock': u'10.0.0.0/16',
                        u'gatewayId': u'local',
                        u'state': u'active'},
                       {u'destinationCidrBlock': u'0.0.0.0/0',
                        u'instanceId': u'i-6e7ae26d',
                        u'instanceOwnerId': u'478468994184',
                        u'networkInterfaceId': u'eni-193a7e70',
                        u'state': u'active'}],
         u'routeTableId': u'rtb-ac7704c5',
         u'tagSet': [{u'Key':u'Role', u'Value':u'Test Instance'}],
         u'vpcId': u'vpc-aa7704c3'},
        vpcs[0])
    expects = json.dumps({
            "rtbac7704c5": {
                "Type": "AWS::EC2::RouteTable",
                "Properties": {
                    "VpcId" : { "Ref": "vpcaa7704c3" },
                    "Tags" : [{"Key":"Role", "Value": "Test Instance"}]
                    }
                }
            }, sort_keys=True)
    result = json.dumps(route_table, cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects
