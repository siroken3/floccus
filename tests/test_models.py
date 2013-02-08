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
        ),
                   CfnEC2SecurityGroup(
        {'groupDescription': 'External security group',
         'groupId': 'sg-2ce8f440',
         'groupName': 'common-sg',
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

subnets = [
    CfnEC2Subnet(
        {u'availabilityZone': u'ap-northeast-1a',
         u'availableIpAddressCount': 249,
         u'cidrBlock': u'10.0.1.0/24',
         u'state': u'available',
         u'subnetId': u'subnet-78760511',
         u'vpcId': u'vpc-aa7704c3'},
        vpcs[0]
        ),
    CfnEC2Subnet(
        {u'availabilityZone': u'ap-northeast-1a',
         u'availableIpAddressCount': 249,
         u'cidrBlock': u'10.0.2.0/24',
         u'state': u'available',
         u'subnetId': u'subnet-aa7704c3',
         u'vpcId': u'vpc-aa7704c3'},
        vpcs[0]
        ),
    CfnEC2Subnet(
        {u'availabilityZone': u'ap-northeast-1a',
         u'availableIpAddressCount': 249,
         u'cidrBlock': u'10.0.3.0/24',
         u'state': u'available',
         u'subnetId': u'subnet-6776050e',
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
,security_groups, subnets[1])]

iam_groups = [
    CfnIAMGroup(
        {
            u'Group': {
                u'Arn': u'arn:aws:iam::478468994184:group/as',
                u'CreateDate': u'2012-12-18T09:31:19Z',
                u'GroupId': u'321321321321321321321',
                u'GroupName': u'as',
                u'Path': u'/',
                },
            u'Policies': [
                {
                    u'PolicyName': u'policygen-as-YYYYMMDDHHmm',
                    u'PolicyDocument': u'%7B%0A%20%20%22Statement%22%3A%20%5B%0A%20%20%20%20%7B%0A%20%20%20%20%20%20%22Sid%22%3A%20%22Stmt1355830196941%22%2C%0A%20%20%20%20%20%20%22Action%22%3A%20%5B%0A%20%20%20%20%20%20%20%20%22cloudwatch%3A%2A%22%0A%20%20%20%20%20%20%5D%2C%0A%20%20%20%20%20%20%22Effect%22%3A%20%22Allow%22%2C%0A%20%20%20%20%20%20%22Resource%22%3A%20%5B%0A%20%20%20%20%20%20%20%20%22%2A%22%0A%20%20%20%20%20%20%5D%0A%20%20%20%20%7D%2C%0A%20%20%20%20%7B%0A%20%20%20%20%20%20%22Sid%22%3A%20%22Stmt1355830207207%22%2C%0A%20%20%20%20%20%20%22Action%22%3A%20%5B%0A%20%20%20%20%20%20%20%20%22autoscaling%3A%2A%22%0A%20%20%20%20%20%20%5D%2C%0A%20%20%20%20%20%20%22Effect%22%3A%20%22Allow%22%2C%0A%20%20%20%20%20%20%22Resource%22%3A%20%5B%0A%20%20%20%20%20%20%20%20%22%2A%22%0A%20%20%20%20%20%20%5D%0A%20%20%20%20%7D%0A%20%20%5D%0A%7D',
                    u'GroupName': u'as',
                    }
                ]
            })
    ]

iam_roles = [CfnIAMRole(
        {u'Arn': u'arn:aws:iam::478468994184:role/LogServerRole',
         u'AssumeRolePolicyDocument': u'%7B%22Version%22%3A%222008-10-17%22%2C%22Statement%22%3A%5B%7B%22Sid%22%3A%22%22%2C%22Effect%22%3A%22Allow%22%2C%22Principal%22%3A%7B%22Service%22%3A%22ec2.amazonaws.com%22%7D%2C%22Action%22%3A%22sts%3AAssumeRole%22%7D%5D%7D',
         u'CreateDate': u'2012-11-19T12:38:03Z',
         u'Path': u'/',
         u'RoleId': u'AROAJ25JKW56LCC73JH74',
         u'RoleName': u'LogServerRole'})
]

iam_users = [CfnIAMUser({}, iam_groups)
]

instance_profiles = [
    CfnIAMInstanceProfile(
        {u'Arn': u'arn:aws:iam::478468994184:instance-profile/LogServerRole',
         u'CreateDate': u'2012-11-19T12:38:03Z',
         u'InstanceProfileId': u'123456789012345123456',
         u'InstanceProfileName': u'LogServerRole',
         u'Path': u'/', 
         u'Roles': [{u'Arn': u'arn:aws:iam::478468994184:role/LogServerRole',
                     u'AssumeRolePolicyDocument': u'%7B%22Version%22%3A%222008-10-17%22%2C%22Statement%22%3A%5B%7B%22Sid%22%3A%22%22%2C%22Effect%22%3A%22Allow%22%2C%22Principal%22%3A%7B%22Service%22%3A%22ec2.amazonaws.com%22%7D%2C%22Action%22%3A%22sts%3AAssumeRole%22%7D%5D%7D',
                     u'CreateDate': u'2012-11-19T12:38:03Z',
                     u'Path': u'/',
                     u'RoleId': u'AROAJ25JKW56LCC73JH74',
                     u'RoleName': u'LogServerRole'}
                    ]}, iam_roles)
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
    expects = json.dumps({
            "subnet78760511": {
                "Type": "AWS::EC2::Subnet",
                "Properties": {
                    "AvailabilityZone" : "ap-northeast-1a",
                    "CidrBlock": "10.0.1.0/24",
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
        "sg28e8f444" : {
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


def test_iam_group():
    expects = json.dumps({
            "as": {
                "Type": "AWS::IAM::Group",
                "Properties": {
                    "Path": "/",
                    "Policies": [{
                            "PolicyName": "policygen-as-YYYYMMDDHHmm",
                            "PolicyDocument": {
                                "Statement": [
                                    {
                                        "Sid": "Stmt1355830196941",
                                        "Action": [
                                            "cloudwatch:*"
                                            ],
                                        "Effect": "Allow",
                                        "Resource": [
                                            "*"
                                            ]
                                        },
                                    {
                                        "Sid": "Stmt1355830207207",
                                        "Action": [
                                            "autoscaling:*"
                                            ],
                                        "Effect": "Allow",
                                        "Resource": [
                                            "*"
                                            ]
                                        }
                                    ]
                                }
                        }]
                    }
                }
            }, sort_keys=True)
    result = json.dumps(iam_groups[0], cls=CfnJsonEncoder, sort_keys=True)
    print 'result = ', result
    print 'expects= ', expects
    assert result == expects

def test_iam_instance_profile():
    expects = json.dumps({
            "LogServerRole": {
                "Type":"AWS::IAM::InstanceProfile",
                "Properties": {
                    "Path": "/",
                    "Roles": [{"Ref": "LogServerRole"}]
                    }
                }
            }, sort_keys=True)
    result = json.dumps(instance_profiles[0], cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_iam_role():
    expects = json.dumps({
            "LogServerRole": {
                "Type": "AWS::IAM::Role",
                "Properties": {
                    "AssumeRolePolicyDocument": {
                        "Statement": [
                            {"Action": "sts:AssumeRole", "Effect": "Allow",
                             "Principal": {"Service": "ec2.amazonaws.com"},
                             "Sid": ""}],
                        "Version": "2008-10-17"
                        },
                    "Path": "/",
                    "Policies": []
                    }
                }
            }, sort_keys=True)
    result = json.dumps(iam_roles[0], cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def _test_iam_user():
    expects = json.dumps({
            "": {
                "Type":"AWS::IAM::User",
                "Properties": {
                    "Path": "",
                    "Groups": [],
                    "LoginProfile": { "Password": "" },
                    "Policies": []
                    }
                }
            }, sort_keys=True)
    result = json.dumps(iam_users[0], cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_networkinterface():
    expects = json.dumps({
            "enid97b08b0": {
                "Type": "AWS::EC2::NetworkInterface",
                "Properties":{
                    "Description": "ELB keshin-stg",
                    "GroupSet": [ {"Ref":"sg28e8f444"} ],
                    "PrivateIpAddress": "10.0.0.31",
                    "SourceDestCheck": True,
                    "SubnetId": {"Ref":"subnetaa7704c3"},
                    "Tags": []
                    }
                }
            }, sort_keys=True)
    result = json.dumps(network_interfaces[0], cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects


def test_instance():
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
        instance_profiles[0],
        network_interfaces,
        security_groups,
        subnets[2]
        )

    expects = json.dumps({
            "if26de9f1":{
                "Type": "AWS::EC2::Instance",
                "Properties" : {
                    "AvailabilityZone" : "ap-northeast-1a",
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
                    "IamInstanceProfile": { "Ref": "LogServerRole" },
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
                    "Volumes": []
                    }
                }
            },sort_keys=True)
    result = json.dumps(instance, cls=CfnJsonEncoder, sort_keys=True)
    print "expect = ", expects
    print ""
    print "result = ", result
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
