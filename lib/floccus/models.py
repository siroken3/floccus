# -*- coding:utf-8 -*-

from json import JSONEncoder
import utils

class CfnJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, CfnAWSObject):
            return o._cfn_expr()
        return JSONEncoder.default(self, o)


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
                properties[entrykey] = getattr(self, entrykey)
            except KeyError:
                pass
        return properties


class CfnAWSResource(CfnAWSDataType):
    def __init__(self, api_response, resource_type):
        CfnAWSDataType.__init__(self, api_response)
        self._resource_type = resource_type

    def _name(self):
        return utils.normalize_name(self._cfn_id())

    def _resource_properties(self):
        properties = {}
        entrykeys = [p for p in dir(self) if not p.startswith('_')]
        for entrykey in entrykeys:
            try:
                properties[entrykey] = getattr(self, entrykey)
            except KeyError:
                pass
        return properties

    def _cfn_expr(self):
        return {
            self._name(): {
                "Type": self._resource_type,
                "Properties": self._resource_properties()
                }
            }


class CfnAWSResourceRef(CfnAWSObject):
    def __init__(self, cfn_resource):
        self.cfn_resource = cfn_resource

    def _cfn_id(self):
        return self.cfn_resource._cfn_id()

    def _cfn_expr(self):
        return { 'Ref': self.cfn_resource._name() }


class CfnTaggedResource(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, vpc)


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
    def __init__(self, api_response, cfn_vpc, cfn_internet_gateways):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::VPCGatewayAttachment")
        self._vpc = CfnAWSResourceRef(cfn_vpc)
        for cfn_igw in cfn_internet_gateways:
            if self._get_api_response('internetGatewayId') == cfn_igw._cfn_id():
                self._internet_gateway = CfnAWSResourceRef(cfn_igw)
                break

    def _cfn_id(self):
        return self._vpc._cfn_id() + self._internet_gateway._cfn_id()

    @property
    def InternetGatewayId(self):
        return self._internet_gateway

    @property
    def VpcId(self):
        return self._vpc


class CfnEC2Subnet(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::Subnet")
        self.__vpc = CfnAWSResourceRef(cfn_vpc)

    def _cfn_id(self):
        return self._get_api_response('subnetId')

    @property
    def AvailabilityZone(self):
        return self._get_api_response('availabilityZone')

    @property
    def CidrBlock(self):
        return self._get_api_response('cidrBlock')

    @property
    def VpcId(self):
        return self.__vpc


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

    def __init__(self, api_response, cfn_vpc):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::SecurityGroup")
        self._vpc = CfnAWSResourceRef(cfn_vpc)
        ingresses = []
        for ipPermission in api_response['ipPermissions']:
            ingresses.extend(utils.flatten(ipPermission, 'ipRanges'))
        self._ipPermissions = [self._CfnEC2SecurityGroupRulePropertyType(ingress) for ingress in ingresses]
        egresses = []
        for ipPermission in api_response['ipPermissionsEgress']:
            egresses.extend(utils.flatten(ipPermission, 'ipRanges'))
        self._ipPermissionEgress = [self._CfnEC2SecurityGroupRulePropertyType(egress) for egress in egresses]

    def _cfn_id(self):
        return self._vpc._cfn_id() + self._get_api_response('groupName') + "SecurityGroup"

    @property
    def GroupDescription(self):
        return self._get_api_response('groupDescription')

    @property
    def SecurityGroupIngress(self):
        return self._ipPermissions

    @property
    def SecurityGroupEgress(self):
        return self._ipPermissionEgress

    @property
    def VpcId(self):
        return self._vpc

class CfnIAMInstanceProfile(CfnAWSResource):
    def __init__(self, api_response):
        pass

class CfnRouteTable(CfnAWSResource):
    def __init__(self, api_response, cfn_vpc):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::RouteTable")
        self._vpc = CfnAWSResourceRef(cfn_vpc)

    def _cfn_id(self):
        return self._get_api_response('routeTableId')

    @property
    def VpcId(self):
        return self._vpc

    @property
    def Tags(self):
        return self._get_api_response('tagSet')

class CfnIAMInstanceProfile(CfnAWSResource):
    def __init__(self, api_response):
        CfnAWSResource.__init__(self, api_response, "AWS::IAM::InstanceProfile")

    @property
    def Path(self):
        pass

    @property
    def Roles(self):
        pass

class CfnEC2NetworkInterface(CfnAWSResource):
    def __init__(self,
                 api_response,
                 cfn_security_groups,
                 cfn_subnets):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::NetworkInterface")

    def _cfn_id(self):
        return self._get_api_response('networkInterfaceId')

    @property
    def Description(self):
        return self._get_api_response('description')

    @property
    def GroupSet(self):
        pass

    @property
    def PrivateIpAddress(self):
        return self._get_api_response('privateIpAddress')

    @property
    def SourceDestCheck(self):
        return self._get_api_response('sourceDestCheck')

    @property
    def SubnetId(self):
        pass

    @property
    def Tags(self):
        return self._get_api_response('tagSet')

class CfnEC2Instance(CfnAWSResource):
    class _CfnBlockDeviceMapping(CfnAWSDataType):
        def __init__(self, api_response):
            CfnAWSDataType.__init__(self, api_response)

        @property
        def DeviceName(self):
            pass

        @property
        def Ebs(self):
            pass

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

    def __init__(self,
                 api_response,
                 cfn_instance_profiles,
                 cfn_network_interfaces,
                 cfn_security_groups,
                 cfn_subnets):
        CfnAWSResource.__init__(self, api_response, "AWS::EC2::Instance")
        self._instance_profile = CfnAWSResourceRef(cfn_instance_profiles)
        self._network_interfaces = [CfnAWSResourceRef(eni) for eni in cfn_network_interfaces]
        self._security_groups = [CfnAWSResourceRef(sg) for sg in cfn_security_groups]
        self._subnet = CfnAWSResourceRef(cfn_subnets)

    def _cfn_id(self):
        return self._get_api_response('instanceId')

    @property
    def AvailabilityZone(self):
        pass

    @property
    def BlockDeviceMappings(self):
        pass

    @property
    def DisableApiTermination(self):
        pass

    @property
    def EbsOptimized(self):
        pass

    @property
    def IamInstanceProfile(self):
        return self._instance_profile

    @property
    def ImageId(self):
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
    def Monitoring(self):
        pass

    @property
    def NetworkInterfaces(self):
        return self._network_interfaces

    @property
    def PlacementGroupName(self):
        pass

    @property
    def PrivateIpAddress(self):
        pass

    @property
    def RamdiskId(self):
        pass

    @property
    def SecurityGroupIds(self):
        pass

    @property
    def SecurityGroups(self):
        return self._security_groups

    @property
    def SourceDestCheck(self):
        pass

    @property
    def SubnetId(self):
        return self._subnet

    @property
    def Tags(self):
        pass

    @property
    def Tenancy(self):
        pass

    @property
    def UserData(self):
        pass

    @property
    def Volumes(self):
        pass

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
