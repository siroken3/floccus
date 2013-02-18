# -*- coding:utf-8 -*-

import urllib
import json

import floccus.utils as utils

class CfnJsonEncoder(json.JSONEncoder):
    def default(self, o):
        print o
        if isinstance(o, CfnAWSObject):
            return o._cfn_expr()
        return json.JSONEncoder.default(self, o)

class CfnAWSObject(object):
    def _cfn_expr(self):
        pass

class CfnAWSDataType(CfnAWSObject):
    def __init__(self, api_response):
        self.__api_response = api_response

    def _has_api_response(self, key):
        return self.__api_response.has_key(key)

    def _get_api_response(self, name):
        return self.__api_response[name]

    def _resource_properties(self):
        properties = {}
        entrykeys = [p for p in dir(self) if not p.startswith('_')]
        for entrykey in entrykeys:
            try:
                attr = getattr(self, entrykey)
                if attr is not None:
                    properties[entrykey] = attr
            except KeyError:
                pass
        return properties

    def _cfn_expr(self):
        return self._resource_properties()


class CfnAWSResource(CfnAWSDataType):
    def __init__(self, api_response, resource_type):
        CfnAWSDataType.__init__(self, api_response)
        self._resource_type = resource_type

    def _name(self):
        return utils.normalize_name(self._cfn_id())

    def _cfn_expr(self):
        return {
            self._name(): {
                "Type": self._resource_type,
                "Properties": self._resource_properties()
                }
            }

def cfn_resourceref(ref_id):
    return { 'Ref': utils.normalize_name(str(ref_id)) }


class CfnVpc(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, 'AWS::EC2::VPC')

    def _cfn_id(self):
        return self._get_api_response('vpcId')

    @property
    def CidrBlock(self):
        return self._get_api_response('cidrBlock')

    @property
    def InstanceTenancy(self):
        return self._get_api_response('instanceTenancy')

class CfnInternetGateway(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::InternetGateway")

    def _cfn_id(self):
        return self._get_api_response('internetGatewayId')

    @property
    def Tags(self):
        return self._get_api_response('tagSet')


class CfnInternetGatewayAttachment(CfnAWSResource):
    def __init__(self, api_response, gateway_id):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::VPCGatewayAttachment")
        self._vpc = cfn_resourceref(api_response['vpcId'])
        self._internet_gateway = cfn_resourceref(gateway_id)
        self._gateway_id = gateway_id

    def _cfn_id(self):
        return self._get_api_response('vpcId') + self._gateway_id

    @property
    def InternetGatewayId(self):
        return self._internet_gateway

    @property
    def VpcId(self):
        return self._vpc


class CfnEC2Subnet(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::Subnet")

    def _cfn_id(self):
        return self._get_api_response('subnetId')

    @property
    def AvailabilityZone(self):
        return self._get_api_response('availabilityZone')

    @property
    def CidrBlock(self):
        return self._get_api_response('cidrBlock')

    @property
    def Tags(self):
        return self._get_api_response('tagSet')

    @property
    def VpcId(self):
        return cfn_resourceref(self._get_api_response('vpcId'))


class CfnEC2SecurityGroup(CfnAWSResource):
    class _CfnEC2SecurityGroupRulePropertyType(CfnAWSDataType):
        def _cfn_expr(self):
            return self._resource_properties()

        @property
        def IpProtocol(self):
            return self._get_api_response('ipProtocol')

        @property
        def CidrIp(self):
            return self._get_api_response('cidrIp')

        @property
        def FromPort(self):
            if self._has_api_response('fromPort'):
                return str(self._get_api_response('fromPort'))
            else:
                return "0"

        @property
        def ToPort(self):
            if self._has_api_response('toPort'):
                return str(self._get_api_response('toPort'))
            else:
                return "65536"

    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::SecurityGroup")

        ingresses = []
        for ipPermission in api_response['ipPermissions']:
            ingresses.extend(utils.flatten(ipPermission, 'ipRanges'))
        self._ipPermissions = [self._CfnEC2SecurityGroupRulePropertyType(ingress)._cfn_expr() for ingress in ingresses]

        egresses = []
        for ipPermission in api_response['ipPermissionsEgress']:
            egresses.extend(utils.flatten(ipPermission, 'ipRanges'))
        self._ipPermissionEgress = [self._CfnEC2SecurityGroupRulePropertyType(egress)._cfn_expr() for egress in egresses]

    def _cfn_id(self):
        return self._get_api_response('groupId')

    @property
    def GroupDescription(self):
        return self._get_api_response('groupDescription')

    @property
    def SecurityGroupEgress(self):
        return self._ipPermissionEgress

    @property
    def SecurityGroupIngress(self):
        return self._ipPermissions

    @property
    def VpcId(self):
        return cfn_resourceref(self._get_api_response('vpcId'))

class CfnEC2RouteTable(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::RouteTable")

    def _cfn_id(self):
        return self._get_api_response('routeTableId')

    @property
    def VpcId(self):
        return cfn_resourceref(self._get_api_response('vpcId'))

    @property
    def Tags(self):
        return self._get_api_response('tagSet')

class CfnIAMInstanceProfile(CfnAWSResource):
    def __init__(self, api_response, cfn_iam_roles):
        CfnAWSResource.__init__(self, api_response, "AWS::IAM::InstanceProfile")
        self._roles = [CfnAWSResourceRef(role) for role in cfn_iam_roles]

    def _cfn_id(self):
        return self._get_api_response('InstanceProfileName')

    @property
    def Path(self):
        return self._get_api_response('Path')

    @property
    def Roles(self):
        return self._roles

class CfnEC2NetworkInterface(CfnAWSResource):
    def __init__(self,
                 api_response,
                 cfn_security_groups,
                 cfn_subnet):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::NetworkInterface")
        self._security_groups = [CfnAWSResourceRef(sg) for sg in cfn_security_groups]
        self._subnet = CfnAWSResourceRef(cfn_subnet)

    def _cfn_id(self):
        return self._get_api_response('networkInterfaceId')

    @property
    def Description(self):
        return self._get_api_response('description')

    @property
    def GroupSet(self):
        return self._security_groups

    @property
    def PrivateIpAddress(self):
        return self._get_api_response('privateIpAddress')

    @property
    def SourceDestCheck(self):
        return self._get_api_response('sourceDestCheck')

    @property
    def SubnetId(self):
        return self._subnet

    @property
    def Tags(self):
        return self._get_api_response('tagSet')

class CfnEC2Instance(CfnAWSResource):
    class _CfnBlockDeviceMapping(CfnAWSDataType):
        class _CfnBlockDeviceProperty(CfnAWSDataType):
            def __init__(self, api_response):
                CfnAWSDataType.__init__(self, api_response)

            @property
            def DeleteOnTermination(self):
                return self._get_api_response('deleteOnTermination')

            @property
            def Iops(self):
                pass

            @property
            def Size(self):
                return None

            @property
            def SnapshotId(self):
                return None

            @property
            def VolumnType(self):
                return None

        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)
            self._ebs = self._CfnBlockDeviceProperty(api_response['ebs'])._cfn_expr()

        @property
        def DeviceName(self):
            return self._get_api_response('deviceName')

        @property
        def Ebs(self):
            return self._ebs

        @property
        def NoDevice(self):
            pass

        @property
        def VirtualName(self):
            pass


    class _CfnMountPoint(CfnAWSDataType):
        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)

        @property
        def Device(self):
            pass

        @property
        def VolumeId(self):
            pass

    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::Instance")

    def _cfn_id(self):
        return self._get_api_response('instanceId')

    @property
    def AvailabilityZone(self):
        return self._get_api_response('placement')['availabilityZone']

    @property
    def BlockDeviceMappings(self):
        api_response = self._get_api_response('blockDeviceMapping')
        blockdeviceMappings = [self._CfnBlockDeviceMapping(bdm)._cfn_expr() for bdm in api_response]
        return blockdeviceMappings

    @property
    def DisableApiTermination(self):
        return self._get_api_response('disableApiTermination')

    @property
    def EbsOptimized(self):
        return self._get_api_response('ebsOptimized')

    @property
    def IamInstanceProfile(self):
        return cfn_resourceref(self._get_api_response('iamInstanceProfile')['id'])

    @property
    def ImageId(self):
        return self._get_api_response('imageId')

    @property
    def InstanceType(self):
        return self._get_api_response('instanceType')

    @property
    def KernelId(self):
        return self._get_api_response('kernelId')

    @property
    def KeyName(self):
        return self._get_api_response('keyName')

    @property
    def Monitoring(self):
        monitoring_state = self._get_api_response('monitoring')['state']
        if monitoring_state == 'disabled':
            return False
        else:
            return True

    @property
    def NetworkInterfaces(self):
        api_response = self._get_api_response('networkInterfaceSet')
        network_interfaces = [cfn_resourceref(eni['networkInterfaceId']) for eni in api_response]
        return network_interfaces

    @property
    def PlacementGroupName(self):
        return self._get_api_response('placement')['groupName']

    @property
    def PrivateIpAddress(self):
        return self._get_api_response('privateIpAddress')

    @property
    def RamdiskId(self):
        return self._get_api_response('ramdiskId')

    @property
    def SecurityGroupIds(self):
        api_response = self._get_api_response('groupSet')
        security_groups = [cfn_resourceref(sg['groupId']) for sg in api_response]
        return security_groups

    @property
    def SecurityGroups(self):
        return []

    @property
    def SourceDestCheck(self):
        return self._get_api_response('sourceDestCheck')

    @property
    def SubnetId(self):
        return cfn_resourceref(self._get_api_response('subnetId'))

    @property
    def Tags(self):
        return self._get_api_response('tagSet')

    @property
    def Tenancy(self):
        return self._get_api_response('placement')['tenancy']

    @property
    def UserData(self):
        return self._get_api_response('userData')

    @property
    def Volumes(self):
        return []

class CfnEC2Volume(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::Volume")

    def _cfn_id(self):
        return self._get_api_response('volumeId')

    @property
    def AvailabilityZone(self):
        return self._get_api_response('availabilityZone')

    @property
    def Iops(self):
        return self._get_api_response('iops')

    @property
    def Size(self):
        return self._get_api_response('size')

    @property
    def SnapshotId(self):
        return self._get_api_response('snapshotId')

    @property
    def Tags(self):
        return self._get_api_response('tagSet')

    @property
    def VolumnType(self):
        return self._get_api_response('volumneType')

class CfnEC2VolumeAttachment(CfnAWSResource):
    def __init__(self, api_response, volume_id):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::VolumeAttachment")
        self._volume_id = volume_id

    def _cfn_id(self):
        return self._volume_id + self._get_api_response('instanceId')

    @property
    def Device(self):
        return self._get_api_response('device')

    @property
    def InstanceId(self):
        return cfn_resourceref(self._get_api_response('instanceId'))

    @property
    def VolumeId(self):
        return cfn_resourceref(self._volume_id)

class CfnSubnetRouteTableAssociation(CfnAWSResource):
    def __init__(self,
                 api_response,
                 cfn_route_table,
                 cfn_subnet):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::SubnetRouteTableAssociation")
        self._route_table = CfnAWSResourceRef(cfn_route_table)
        self._subnet = CfnAWSResourceRef(cfn_subnet)

    @property
    def RouteTableId(self):
        return self._route_table

    @property
    def SubnetId(self):
        return self._subnet

class CfnRoute(CfnAWSResource):
    def __init__(self,
                 api_response,
                 cfn_route_table,
                 cfn_gateway=None,
                 cfn_instance=None,
                 cfn_network_interface=None):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::Route")
        self._gateway = CfnAWSResourceRef(cfn_gateway)
        self._instance = CfnAWSResourceRef(cfn_instance)
        self._network_interface = CfnAWSResourceRef(cfn_network_interface)
        self._route_table = CfnAWSResourceRef(cfn_route_table)

    @property
    def DestinationCidrBlock(self):
        pass

    @property
    def GatewayId(self):
        return self._gateway

    @property
    def InstanceId(self):
        return self._instance

    @property
    def NetworkInterfaceId(self):
        return self._network_interface

    @property
    def RouteTableId(self):
        return self._route_table


class CfnAutoScalingLaunchConfiguration(CfnAWSResource):
    def __init__(self, api_response, cfn_security_groups):
        CfnAWSResource.__init__(self, api_response, "AWS::AutoScaling::LaunchConfiguration")

    @property
    def BlockDeviceMappings(self):
        pass

    @property
    def IamInstanceProfile(self):
        pass

    @property
    def ImageId(self):
        pass

    @property
    def InstanceMonitoring(self):
        pass

    @property
    def InstanceType(self):
        pass

    @property
    def KernelId(self):
        pass

    @property
    def KeyName(self):
        pass

    @property
    def RamDiskId(self):
        pass

    @property
    def SecurityGroups(self):
        pass

    @property
    def SpotPrice(self):
        pass

    @property
    def UserData(self):
        pass


class CfnAutoScalingGroup(CfnAWSResource):
    def __init__(self, api_response, cfn_launch_configuration, cfn_subnets):
        CfnAWSResource.__init__(self, api_response, "AWS::AutoScaling::AutoScalingGroup")


class CfnAutoScalingNotificationConfigurationPropertyType(CfnAWSDataType):
    def __init__(self, api_response):
        CfnAWSDataType.__init__(self, api_response)


class CfnAutoScalingPolicy(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::AutoScaling::ScalingPolicy")

class CfnSNSSubscriptionPropertyType(CfnAWSDataType):
    def __init__(self, api_response):
        CfnAWSDataType.__init__(self, api_response)

    @property
    def Endpoint(self):
        pass

    @property
    def Protocol(self):
        pass

class CfnSNSTopic(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::SNS::Topic")

class CfnRDSDBInstance(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::RDS::DBInstance")

class CfnIAMGroup(CfnAWSResource):
    class _GetGroupPolicyResult(CfnAWSDataType):
        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)

#        def GroupName(self):
#            return self._get_api_response('GroupName')

        @property
        def PolicyDocument(self):
            documentstr = urllib.unquote(self._get_api_response('PolicyDocument'))
            return json.loads(documentstr)

        @property
        def PolicyName(self):
            return self._get_api_response('PolicyName')

    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::IAM::Group")
        self._policies = [self._GetGroupPolicyResult(policy) for policy in self._get_api_response('Policies')]

    def _cfn_id(self):
        return self._get_api_response('Group')['GroupName']

    @property
    def Path(self):
        return self._get_api_response('Group')['Path']

    @property
    def Policies(self):
        return self._policies

class CfnIAMRole(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::IAM::Role")
        self._policies = []

    def _cfn_id(self):
        return self._get_api_response('RoleName')

    @property
    def AssumeRolePolicyDocument(self):
        documentstr = urllib.unquote(self._get_api_response('AssumeRolePolicyDocument'))
        return json.loads(documentstr)

    @property
    def Path(self):
        return self._get_api_response('Path')

    @property
    def Policies(self):
        return self._policies

class CfnIAMUser(CfnAWSResource):
    def __init__(self, api_response, cfn_iam_groups):
        CfnAWSResource.__init__(self, api_response, "AWS::IAM::User")
