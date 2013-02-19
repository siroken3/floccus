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


class CfnEC2NetworkInterface(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::NetworkInterface")

    def _cfn_id(self):
        return self._get_api_response('networkInterfaceId')

    @property
    def Description(self):
        return self._get_api_response('description')

    @property
    def GroupSet(self):
        security_groups = self._get_api_response('groupSet')
        return [cfn_resourceref(sg['groupId']) for sg in security_groups]

    @property
    def PrivateIpAddress(self):
        return self._get_api_response('privateIpAddress')

    @property
    def SourceDestCheck(self):
        return self._get_api_response('sourceDestCheck')

    @property
    def SubnetId(self):
        return cfn_resourceref(self._get_api_response('subnetId'))

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
        pass

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
    def __init__(self, api_response, route_table_id):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::SubnetRouteTableAssociation")
        self._route_table_id = route_table_id

    def _cfn_id(self):
        return self._get_api_response('routeTableAssociationId')

    @property
    def RouteTableId(self):
        return cfn_resourceref(self._route_table_id)

    @property
    def SubnetId(self):
        return cfn_resourceref(self._get_api_response('subnetId'))

class CfnEC2Route(CfnAWSResource):
    def __init__(self, api_response, route_table_id):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::Route")
        self._route_table_id = route_table_id

    def _cfn_id(self):
        return self._route_table_id + self._get_api_response('destinationCidrBlock')

    @property
    def DestinationCidrBlock(self):
        return self._get_api_response('destinationCidrBlock')

    @property
    def GatewayId(self):
        return cfn_resourceref(self._get_api_response('gatewayId'))

    @property
    def InstanceId(self):
        return cfn_resourceref(self._get_api_response('instanceId'))

    @property
    def NetworkInterfaceId(self):
        return cfn_resourceref(self._get_api_response('networkInterfaceId'))

    @property
    def RouteTableId(self):
        return cfn_resourceref(self._route_table_id)


class CfnAutoScalingLaunchConfiguration(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::AutoScaling::LaunchConfiguration")

    def _cfn_id(self):
        return self._get_api_response('LaunchConfigurationName')

    @property
    def BlockDeviceMappings(self):
        pass

    @property
    def IamInstanceProfile(self):
        return self._get_api_response('iamInstanceProfile')

    @property
    def ImageId(self):
        return self._get_api_response('imageId')

    @property
    def InstanceMonitoring(self):
        return self._get_api_response('InstanceMonitoring')['Enabled']

    @property
    def InstanceType(self):
        return self._get_api_response('InstanceType')

    @property
    def KernelId(self):
        return self._get_api_response('KernelId')

    @property
    def KeyName(self):
        return self._get_api_response('KeyName')

    @property
    def RamDiskId(self):
        return self._get_api_response('RamdiskId')

    @property
    def SecurityGroups(self):
        return [cfn_resourceref(sg) for sg in self._get_api_response('SecurityGroups')]

    @property
    def SpotPrice(self):
        return self._get_api_response('SpotPrice')

    @property
    def UserData(self):
        return self._get_api_response('UserData')


class CfnAutoScalingAutoScalingGroup(CfnAWSResource):
    class _CfnAutoScalingNotificationConfigurationPropertyType(CfnAWSDataType):
        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)

        @property
        def TopicARN(self):
            return self._get_api_response('TopicARN')

        @property
        def NotificationTypes(self):
            return self._get_api_response('NotificationType')

    def __init__(self, api_response, notification_configurations):
        CfnAWSResource.__init__(self, api_response, "AWS::AutoScaling::AutoScalingGroup")
        ncs = [nc for nc in notification_configurations if nc['AutoScalingGroupName'] == api_response['AutoScalingGroupName']]
        # TopicARN must be unique
        if len(ncs) >= 1:
            self._notification_configuration = self._CfnAutoScalingNotificationConfigurationPropertyType(utils.groupby(ncs, "TopicARN", "NotificationType")[0])._cfn_expr()
        else:
            self._notification_configuration = []

    def _cfn_id(self):
        return self._get_api_response('AutoScalingGroupName')

    @property
    def AvailabilityZones(self):
        return self._get_api_response('AvailabilityZones')

    @property
    def Cooldown(self):
        return self._get_api_response('DefaultCooldown')

    @property
    def DesiredCapacity(self):
        return self._get_api_response('DesiredCapacity')

    @property
    def HealthCheckGracePeriod(self):
        return self._get_api_response('HealthCheckGracePeriod')

    @property
    def HealthCheckType(self):
        return self._get_api_response('HealthCheckType')

    @property
    def LaunchConfigurationName(self):
        return self._get_api_response('LaunchConfigurationName')

    @property
    def LoadBalancerNames(self):
        return self._get_api_response('LoadBalancerNames')

    @property
    def MaxSize(self):
        return self._get_api_response('MaxSize')

    @property
    def MinSize(self):
        return self._get_api_response('MinSize')

    @property
    def NotificationConfiguration(self):
        return self._notification_configuration

    @property
    def Tags(self):
        return self._get_api_response('Tags')

    @property
    def VPCZoneIdentifier(self):
        return cfn_resourceref(self._get_api_response('VPCZoneIdentifier'))


class CfnAutoScalingPolicy(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::AutoScaling::ScalingPolicy")

    def _cfn_id(self):
        return self._get_api_response('PolicyName')

    @property
    def AdjustmentType(self):
        return self._get_api_response('AdjustmentType')

    @property
    def AutoScalingGroupName(self):
        return self._get_api_response('AutoScalingGroupName')

    @property
    def Cooldown(self):
        return str(self._get_api_response('Cooldown'))

    @property
    def ScalingAdjustment(self):
        return str(self._get_api_response('ScalingAdjustment'))


class CfnSNSTopic(CfnAWSResource):
    class _CfnSNSSubscriptionPropertyType(CfnAWSDataType):
        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)

        @property
        def Endpoint(self):
            return self._get_api_response('Endpoint')

        @property
        def Protocol(self):
            return self._get_api_response('Protocol')

    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::SNS::Topic")
        self._subscription = [self._CfnSNSSubscriptionPropertyType(sb)._cfn_expr() for sb in api_response['Subscriptions']]

    def _cfn_id(self):
        return self._get_api_response('TopicArn')

    @property
    def DisplayName(self):
        return self._get_api_response('DisplayName')

    @property
    def Subscription(self):
        return self._subscription

class CfnRDSDBInstance(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::RDS::DBInstance")


class CfnIAMInstanceProfile(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::IAM::InstanceProfile")

    def _cfn_id(self):
        return self._get_api_response('InstanceProfileName')

    @property
    def Path(self):
        return self._get_api_response('Path')

    @property
    def Roles(self):
        return []


class CfnIAMRole(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::IAM::Role")

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
        pass # A policies are always defined externally.

class CfnIAMPolicy(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::IAM::Policy")

    def _cfn_id(self):
        return self._get_api_response('PolicyName')

    @property
    def Groups(self):
        pass # It does not implement here yet.

    @property
    def PolicyDocument(self):
        documentstr = urllib.unquote(self._get_api_response('PolicyDocument'))
        return json.loads(documentstr)

    @property
    def PolicyName(self):
        return self._get_api_response('PolicyName')

    @property
    def Roles(self):
        return [cfn_resourceref(r) for r in self._get_api_response('Roles')]

    @property
    def Users(self):
        pass # It does not implement here yet.
