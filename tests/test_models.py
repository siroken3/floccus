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

instance_profiles = [CfnIAMInstanceProfile({})]

security_groups = [CfnEC2SecurityGroup(
        {'groupDescription': 'External security group',
         'groupId': 'sg-28e8f444',
         'groupName': 'external-sg',
         'ipPermissions': [{'fromPort': 22,
                             'groups': [],
                             'ipProtocol': 'tcp',
                             'ipRanges': [{'cidrIp': '123.123.123.123/32'},
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
                             'ipRanges': [{'cidrIp': '123.123.123.123/32'},
                                           {'cidrIp': '221.186.108.105/32'}],
                             'toPort': 8443}],
         'ipPermissionsEgress': [{'groups': [],
                                   'ipProtocol': '-1',
                                   'ipRanges': [{'cidrIp': '0.0.0.0/0'}]}],
         'ownerId': '478468994184',
         'vpcId': 'vpc-aa7704c3'},
        vpcs[0]
        )]

subnets = [CfnEC2Subnet(
        {u'availabilityZone': u'ap-northeast-1a',
         u'availableIpAddressCount': 249,
         u'cidrBlock': u'10.0.3.0/24',
         u'state': u'available',
         u'subnetId': u'subnet-78760511',
         u'vpcId': u'vpc-aa7704c3'},
        vpcs[0]
        )]

network_interfaces = [CfnEC2NetworkInterface(
        {u'association': {u'ipOwnerId': u'amazon-elb',
                          u'publicIp': u'54.249.42.217'},
         u'attachment': {u'attachTime': u'2012-11-19T13:44:31.000Z',
                         u'attachmentId': u'eni-attach-70ba1619',
                         u'deleteOnTermination': False,
                         u'deviceIndex': 1,
                         u'instanceOwnerId': u'amazon-elb',
                         u'status': u'attached'},
         u'availabilityZone': u'ap-northeast-1a',
         u'description': u'ELB keshin-stg',
         u'groupSet': [{u'groupId': u'sg-28e8f444', u'groupName': u'external-sg'}],
         u'macAddress': u'02:c3:48:c6:66:13',
         u'networkInterfaceId': u'eni-d97b08b0',
         u'ownerId': u'478468994184',
         u'privateIpAddress': u'10.0.0.31',
         u'privateIpAddressesSet': [{u'association': {u'ipOwnerId': u'amazon-elb',
                                                      u'publicIp': u'54.249.42.217'},
                                     u'primary': True,
                                     u'privateIpAddress': u'10.0.0.31'}],
         u'requesterId': u'558376794213',
         u'requesterManaged': True,
         u'sourceDestCheck': True,
         u'status': u'in-use',
         u'subnetId': u'subnet-a77704ce',
         u'tagSet': [],
         u'vpcId': u'vpc-aa7704c3'}
,security_groups, subnets)]





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
    result = json.dumps(subnets[0], cls=CfnJsonEncoder, sort_keys=True)
    print result
    print expects
    assert result == expects

def test_security_group_rule_1():
    group_rule = CfnEC2SecurityGroup._CfnEC2SecurityGroupRulePropertyType({
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
    group_rule = CfnEC2SecurityGroup._CfnEC2SecurityGroupRulePropertyType({
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

    expects = json.dumps({
        "vpcaa7704c3externalsgSecurityGroup" : {
            "Type" : "AWS::EC2::SecurityGroup",
            "Properties" : {
                "GroupDescription" : "External security group",
                "SecurityGroupIngress" : [{
                        "IpProtocol" : "tcp",
                        "CidrIp" : "123.123.123.123/32",
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
                        "CidrIp" : "123.123.123.123/32",
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
    result = json.dumps(security_groups[0], cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_networkinterface():
    expects = json.dumps({
            "enod97b08b0": {
                "Type": "AWS::EC2::NetworkInterface",
                "Properties":{
                    "Description": "ELB keshin-stg",
                    "GroupSet": [ {"Ref":"sg28e8f444"} ],
                    "PrivateIpAddress": "10.0.0.31",
                    "SourceDestCheck": True,
                    "SubnetId": {"Ref":"subneta77704ce"},
                    "Tags": []
                    }
                }
            }, sort_keys=True)
    result = json.dumps(network_interfaces[0], cls=CfnJsonEncoder, sort_keys=True)
    print result
    print expects
    assert result == expects


def _test_instance():
    instance = CfnEC2Instance(
        {u'amiLaunchIndex': 0,
         u'architecture': u'x86_64',
         u'blockDeviceMapping': [{u'deviceName': u'/dev/sda',
                                  u'ebs': {u'attachTime': u'2012-11-20T10:00:29.000Z',
                                           u'deleteOnTermination': True,
                                           u'status': u'attached',
                                           u'volumeId': u'vol-bb779e99'}},
                                 {u'deviceName': u'/dev/sdf',
                                  u'ebs': {u'attachTime': u'2012-11-20T10:00:29.000Z',
                                           u'deleteOnTermination': True,
                                           u'status': u'attached',
                                           u'volumeId': u'vol-be779e9c'}}],
         u'clientToken': u'abcXXXXXXXXXXXXXXX',
         u'dnsName': '',
         u'ebsOptimized': False,
         u'groupSet': [{u'groupId': u'sg-28e8f444', u'groupName': u'external-sg'},
                       {u'groupId': u'sg-2ce8f440', u'groupName': u'common-sg'}],
         u'hypervisor': u'xen',
         u'iamInstanceProfile': {u'arn': u'arn:aws:iam::478468994184:instance-profile/MasterServerRole',
                                 u'id': u'AIPAJVKSNSPJ2FIPJE6JY'},
         u'imageId': u'ami-7855ec79',
         u'instanceId': u'i-f26de9f1',
         u'instanceState': {u'code': 16, u'name': u'running'},
         u'instanceType': u'm1.small',
         u'ipAddress': u'54.249.46.150',
         u'kernelId': u'aki-40992841',
         u'keyName': u'katatema',
         u'launchTime': u'2012-11-20T10:00:23.000Z',
         u'monitoring': {u'state': u'disabled'},
         u'networkInterfaceSet': [{u'association': {u'ipOwnerId': u'478468994184',
                                                    u'publicIp': u'54.249.46.150'},
                                   u'attachment': {u'attachTime': u'2012-11-20T10:00:23.000Z',
                                                   u'attachmentId': u'eni-attach-3c973b55',
                                                   u'deleteOnTermination': True,
                                                   u'deviceIndex': 0,
                                                   u'status': u'attached'},
                                   u'description': u'Primary network interface',
                                   u'groupSet': [{u'groupId': u'sg-28e8f444', u'groupName': u'external-sg'},
                                                 {u'groupId': u'sg-2ce8f440', u'groupName': u'common-sg'}],
                                   u'networkInterfaceId': u'eni-4aa6d523',
                                   u'ownerId': u'478468994184',
                                   u'privateIpAddress': u'10.0.1.4',
                                   u'privateIpAddressesSet': {u'item': {u'association': {u'ipOwnerId': u'478468994184',
                                                                                         u'publicIp': u'54.249.46.150'},
                                                                        u'primary': u'true',
                                                                        u'privateIpAddress': u'10.0.1.4'}},
                                   u'sourceDestCheck': True,
                                   u'status': u'in-use',
                                   u'subnetId': u'subnet-6776050e',
                                   u'vpcId': u'vpc-aa7704c3'}],
         u'placement': {u'availabilityZone': u'ap-northeast-1a',
                        u'groupName': '',
                        u'tenancy': u'default'},
         u'privateDnsName': '',
         u'privateIpAddress': u'10.0.1.4',
         u'productCodes': [],
         u'reason': '',
         u'rootDeviceName': u'/dev/sda1',
         u'rootDeviceType': u'ebs',
         u'sourceDestCheck': True,
         u'ramdiskId': u'ramdisk',
         u'subnetId': u'subnet-6776050e',
         u'tagSet': [{u'key': u'Env', u'value': u'prod'},
                     {u'key': u'Name', u'value': u'p001'},
                     {u'key': u'Type', u'value': u'master'}],
         u'virtualizationType': u'paravirtual',
         u'vpcId': u'vpc-aa7704c3'},
        instance_profiles,
        network_interfaces,
        security_groups,
        subnets
        )

    expects = json.dumps({
            "Type": "AWS::EC2::Instance",
            "Properties" : {
                "AvailabilityZone" : "ap-northeast-1",
                "BlockDeviceMappings": [{
                        "DeviceName": "/dev/sda",
                        "Ebs":{
                            "DeleteOnTermination" : True,
                            },
                        },{
                        "DeviceName": "/dev/sdf",
                        "Ebs":{
                            "DeleteOnTermination" : True,
                            },
                        }],
                "EBSOptimized": False,
                "IamInstanceProfile": { "Ref": "AIPAJVKSNSPJ2FIPJE6JY" },
                "ImageId": "ami-7855ec79",
                "InstanceType": "m1.small",
                "KernelId": "aki-40992841",
                "KeyName": "katatema",
                "Monitoring": False,
                "NetworkInterfaces": [{"Ref":"eni4aa6d523"}],
                "PlacementGroupName": "",
                "PrivateIpAddress":"10.0.1.4",
                "RamdiskId":"ramdisk",
                "SecurityGroupIds": [{"Ref":"sg28e8f444"},{"Ref":"sg2ce8f440"}],
                "SecurityGroups":[],
                "SourceDestCheck": True,
                "SubnetId":{ "Ref": "subnet6776050e"},
                "Tags": [{"Key":"Env","Value":"prod"},{"Key":"Name","Value":"p001"},{"Key":"Type","Value":"master"}],
                "Tenancy":"default",
                "UserData":"",
                "Volumes": [
                    ]
                }
            },sort_keys=True)
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
