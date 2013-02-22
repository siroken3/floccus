# -*- coding:utf-8 -*-

import floccus.utils as utils
from floccus.models import CfnAWSResource, CfnAWSDataType, cfn_resourceref

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
#        return self._get_api_response('tagSet')
#        When the produced json file was used, this does not worked.
        pass

class CfnEC2EIP(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::EIP")

    def _cfn_id(self):
        return self._get_api_response('publicIp')

    @property
    def InstanceId(self):
        return cfn_resourceref(self._get_api_response('instanceId'))

    @property
    def Domain(self):
        return self._get_api_response('domain')

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
        return [utils.capitalize_dict(t) for t in self._get_api_response('tagSet') if utils.valid_cfn_tag(t)]

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
        return [utils.capitalize_dict(t) for t in self._get_api_response('tagSet') if utils.valid_cfn_tag(t)]


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
        return str(self._get_api_response('sourceDestCheck'))

    @property
    def SubnetId(self):
        return cfn_resourceref(self._get_api_response('subnetId'))

    @property
    def Tags(self):
        return [utils.capitalize_dict(t) for t in self._get_api_response('tagSet') if utils.valid_cfn_tag(t)]

class CfnEC2Instance(CfnAWSResource):
    class _CfnBlockDeviceMapping(CfnAWSDataType):
        class _CfnBlockDeviceProperty(CfnAWSDataType):
            def __init__(self, api_response):
                CfnAWSDataType.__init__(self, api_response)

            @property
            def DeleteOnTermination(self):
                return str(self._get_api_response('deleteOnTermination'))

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
            def VolumeType(self):
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
            pass # only modifing using Cloudformation

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
        return str(self._get_api_response('ebsOptimized'))

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
            return "False"
        else:
            return "True"

    @property
    def NetworkInterfaces(self):
        api_response = self._get_api_response('networkInterfaceSet')
        network_interfaces = [{
                "NetworkInterfaceId": cfn_resourceref(eni['networkInterfaceId']),
                "DeviceIndex" : eni['attachment']['deviceIndex']
                }
            for eni in api_response]
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
        return [utils.capitalize_dict(t) for t in self._get_api_response('tagSet') if utils.valid_cfn_tag(t)]

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
        return str(self._get_api_response('size'))

    @property
    def SnapshotId(self):
        return self._get_api_response('snapshotId')

    @property
    def Tags(self):
        return [utils.capitalize_dict(t) for t in self._get_api_response('tagSet') if utils.valid_cfn_tag(t)]

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
