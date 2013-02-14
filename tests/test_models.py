# -*- coding:utf-8 -*-

from floccus.models import *
import testdata
import json

def test_vpc():
    expects = json.dumps({
        "vpcaa7704c3":{
            "Type":"AWS::EC2::VPC",
            "Properties": {
                "CidrBlock":"10.0.0.0/16",
                "InstanceTenancy":"default"
                }
            }
        }, sort_keys=True)
    result = json.dumps(testdata.vpcs[0], cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_internetgateway():
    expects = json.dumps({
            "igwa17704c8": {
                "Type":"AWS::EC2::InternetGateway",
                "Properties": {
                    "Tags": []
                    }
                }
            }, sort_keys=True)
    result = json.dumps(testdata.internet_gateways[0], cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_vpcattachment_internetgateway():
    expects = json.dumps({
            "vpcaa7704c3igwa17704c8": {
                "Type": "AWS::EC2::VPCGatewayAttachment",
                "Properties": {
                    "VpcId": { "Ref" : "vpcaa7704c3" },
                    "InternetGatewayId" : { "Ref" : "igwa17704c8" }
                    }
                }
            }, sort_keys=True)
    result = json.dumps(testdata.igwattachments[0], cls=CfnJsonEncoder, sort_keys=True)
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
    result = json.dumps(testdata.subnets[0], cls=CfnJsonEncoder, sort_keys=True)
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
    result = json.dumps(testdata.security_groups[0], cls=CfnJsonEncoder, sort_keys=True)
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
    result = json.dumps(testdata.iam_groups[0], cls=CfnJsonEncoder, sort_keys=True)
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
    result = json.dumps(testdata.instance_profiles[0], cls=CfnJsonEncoder, sort_keys=True)
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
    result = json.dumps(testdata.iam_roles[0], cls=CfnJsonEncoder, sort_keys=True)
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
    result = json.dumps(testdata.iam_users[0], cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_networkinterface():
    expects = json.dumps({
            "enid97b08b0": {
                "Type": "AWS::EC2::NetworkInterface",
                "Properties":{
                    "Description": "ELB keshin-stg",
                    "GroupSet": [ {"Ref":"sg28e8f444"}, {"Ref":"sg2ce8f440"} ],
                    "PrivateIpAddress": "10.0.0.31",
                    "SourceDestCheck": True,
                    "SubnetId": {"Ref":"subnetaa7704c3"},
                    "Tags": []
                    }
                }
            }, sort_keys=True)
    result = json.dumps(testdata.network_interfaces[0], cls=CfnJsonEncoder, sort_keys=True)
    print "expect = ", expects
    print ""
    print "result = ", result
    assert result == expects

def test_instance():
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
                    "DisableApiTermination": False,
                    "EbsOptimized": False,
                    "IamInstanceProfile": { "Ref": "LogServerRole" },
                    "ImageId": "ami-7855ec79",
                    "InstanceType": "m1.small",
                    "KernelId": "aki-40992841",
                    "KeyName": "keyName",
                    "Monitoring": False,
                    "NetworkInterfaces": [{"Ref":"enid97b08b0"}],
                    "PlacementGroupName": "",
                    "PrivateIpAddress":"10.0.1.4",
                    "RamdiskId":"ramdisk",
                    "SecurityGroupIds": [{"Ref":"sg28e8f444"},{"Ref":"sg2ce8f440"}],
                    "SecurityGroups":[],
                    "SourceDestCheck": True,
                    "SubnetId":{ "Ref": "subnet6776050e"},
                    "Tags": [{"key":"Env","value":"prod"},{"key":"Name","value":"p001"},{"key":"Type","value":"master"}],
                    "Tenancy":"default",
                    "UserData":"",
                    "Volumes": []
                    }
                }
            },sort_keys=True)
    result = json.dumps(testdata.instances[0], cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects

def test_route_table():
    expects = json.dumps({
            "rtbac7704c5": {
                "Type": "AWS::EC2::RouteTable",
                "Properties": {
                    "VpcId" : { "Ref": "vpcaa7704c3" },
                    "Tags" : [{"Key":"Role", "Value": "Test Instance"}]
                    }
                }
            }, sort_keys=True)
    result = json.dumps(testdata.route_tables[0], cls=CfnJsonEncoder, sort_keys=True)
    assert result == expects
