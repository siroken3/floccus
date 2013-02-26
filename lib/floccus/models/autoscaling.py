# -*- coding:utf-8 -*-

from floccus.models import CfnAWSResource, CfnAWSDataType, cfn_resourceref

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
        return self._get_api_response('ImageId')

    @property
    def InstanceMonitoring(self):
        return str(self._get_api_response('InstanceMonitoring')['Enabled'])

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
    def RamdiskId(self):
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
        return str(self._get_api_response('DefaultCooldown'))

    @property
    def DesiredCapacity(self):
        return str(self._get_api_response('DesiredCapacity'))

    @property
    def HealthCheckGracePeriod(self):
        return str(self._get_api_response('HealthCheckGracePeriod'))

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
        return str(self._get_api_response('MaxSize'))

    @property
    def MinSize(self):
        return str(self._get_api_response('MinSize'))

    @property
    def NotificationConfiguration(self):
        if len(self._notification_configuration) == 0:
            return None
        return self._notification_configuration

    @property
    def Tags(self):
        return [utils.capitalize_dict(t) for t in self._get_api_response('tagSet') if utils.valid_cfn_tag(t)]

    @property
    def VPCZoneIdentifier(self):
        return [cfn_resourceref(self._get_api_response('VPCZoneIdentifier'))]


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
