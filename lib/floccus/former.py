# -*- coding:utf-8 -*-

import boto
import boto.ec2
import boto.ec2.autoscale
import boto.vpc
import boto.sns
import boto.rds
import argparse

from models import *

class CloudFormer:
    def __init__(self, access_key, secret_key, region_name='us-east-1'):
        self.access_key = access_key if access_key is not None else ''
        self.secret_key = secret_key if secret_key is not None else ''
        self.region = boto.ec2.get_region(
            region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
            )
        self.region_name = region_name

    def form(self):
        self.vpcconn = boto.connect_vpc(
            region=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
            )
        self.asconn = boto.ec2.autoscale.connect_to_region(
            self.region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
            )
        self.snsconn = boto.sns.connect_to_region(
            self.region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
            )
        self.rdsconn = boto.rds.connect_to_region(
            self.region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
            )
        context = {}
        vpcs = self._form_vpc(context)
        for vpc in vpcs:
            internet_gateways     = self._form_internet_gateway(context, vpc)
            subnets               = self._form_subnets(context, vpc)
            security_groups       = self._form_security_groups(context, vpc)
            instances             = self._form_instances(context, vpc, subnets)
            route_tables          = self._form_route_tables(context, vpc)
            launch_configurations = self._form_auto_scaling_launch_configuration(context, security_groups)
            self._form_gateway_attachments(context, vpc, internet_gateways)
            self._form_subnet_route_table_association(context, route_tables, subnets)
            self._form_route(context, route_tables, internet_gateways, instances)
            self._form_auto_scaling_group(context, launch_configurations, subnets)

        policies              = self._form_auto_scaling_policy(context)
        topics                = self._form_sns_topics(context)
        db_instances          = self._form_db_instance(context)
        return context

    def _form_vpc(self, context):
        vpcs = [CfnVpc(vpc) for vpc in self.vpcconn.get_all_vpcs()]
        self._add_cfn_resource_map(context, vpcs)
        context['vpcs'] = vpcs
        return vpcs

    def _form_internet_gateway(self, context, vpc):
        internet_gateways = [
            CfnInternetGateWay(igw)
            for igw in self.vpcconn.get_all_internet_gateways(
                filters=[('attachment.vpc-id', vpc.id)]
                )
            ]
        self._add_cfn_resource_map(context, internet_gateways)
        context['internet_gateways'] = internet_gateways
        return internet_gateways

    def _form_gateway_attachments(self, context, vpc, internet_gateways):
        attachments       = []
        for internet_gateway in internet_gateways:
            attachments.extend([
                    CfnVpcGatewayAttachment(att, cfn_vpc=vpc, cfn_gateway=internet_gateway)
                    for att in internet_gateway.attachments
                    ])
        context['gateway_attachments'] = attachments
        return attachments

    def _form_subnets(self, context, vpc):
        subnets = [
            CfnSubnet(s, vpc)
            for s in self.vpcconn.get_all_subnets(
                filters=[('vpc-id', vpc.id)]
                )
            ]
        self._add_cfn_resource_map(context, subnets)
        context['subnets'] = subnets
        return subnets

    def _form_security_groups(self, context, vpc):
        security_groups = [
            CfnSecurityGroup(sg, vpc)
            for sg in self.vpcconn.get_all_security_groups()
            if sg.vpc_id == vpc.id
            ]
        self._add_cfn_resource_map(context, security_groups)
        context['security_groups'] = security_groups
        return security_groups

    def _form_route_tables(self, context, vpc):
        route_tables = [
            CfnRouteTable(rtb, cfn_vpc=vpc)
            for rtb in self.vpcconn.get_all_route_tables(
                filters=[('vpc-id', vpc.id)]
                )
            ]
        self._add_cfn_resource_map(context, route_tables)
        context['route_tables'] = route_tables
        return route_tables

    def _form_instances(self, context, vpc, subnets):
        instances = []
        for reservation in self.vpcconn.get_all_instances(filters={'vpc-id': vpc.id}):
            for instance in reservation.instances:
                    instances.extend([
                            CfnEC2Instance(instance, cfn_subnet=subnet)
                            for subnet in subnets
                            if subnet.id == instance.subnet_id
                        ])
        self._add_cfn_resource_map(context, instances)
        context['instances'] = instances
        return instances

    def _form_route(self, context, route_tables=[], internet_gateways=[], instances=[], network_interfaces=[]):
        routes             = []
        for route_table in route_tables:
            for gateway in internet_gateways:
                routes.extend([
                        CfnRoute(route, cfn_route_table=route_table, cfn_gateway=gateway)
                        for route in route_table.routes
                        if gateway.id == route.gateway_id
                     ])
            for instance in instances:
                routes.extend([
                        CfnRoute(route, cfn_route_table=route_table, cfn_instance=instance)
                        for route in route_table.routes
                        if instance.id == route.instance_id
                        ])
            for network_interface in network_interfaces:
                routes.extend([
                        CfnRoute(route, cfn_route_table=route_table, cfn_network_interface=network_interface)
                        for route in route_table.routes
                        if network_interfaces.id == route.network_interface_id
                        ])
        context['routes'] = routes
        return routes

    def _form_subnet_route_table_association(self, context, route_tables, subnets):
        associations = []
        for subnet in subnets:
            for route_table in route_tables:
                associations.extend([
                        CfnSubnetRouteTableAssociation(assoc, cfn_route_table=route_table, cfn_subnet=subnet)
                        for assoc in route_table.associations
                        if assoc.subnet_id == subnet.id
                        ])
        self._add_cfn_resource_map(context, associations)
        context['subnet_route_table_associations'] = associations
        return associations

    def _form_auto_scaling_launch_configuration(self, context, cfn_security_groups):
        configurations = []
        for lc in self.asconn.get_all_launch_configurations():
            lc_sgs = lc.security_groups
            target_cfn_sg_groups = [cfn_sg_group for cfn_sg_group in cfn_security_groups if cfn_sg_group.id in lc_sgs]
            configurations.extend([CfnAutoScalingLaunchConfiguration(lc, target_cfn_sg_groups)])
        context['launch_configurations'] = configurations
        return configurations

    def _form_auto_scaling_group(self, context, launch_configurations, subnets):
        groups = []
        for asg in self.asconn.get_all_groups():
            zone_ids = asg.vpc_zone_identifier.split(',')
            cfn_subnets = [s for s in subnets if s.id in zone_ids]
            for lc in launch_configurations:
                if asg.launch_config_name == lc.name:
                    groups.extend([
                    CfnAutoScalingGroup(asg, cfn_launch_configuration=lc, cfn_subnets=cfn_subnets)
                    ])
        context['auto_scaling_groups'] = groups
        return groups

    def _form_auto_scaling_policy(self, context):
        auto_scaling_policies = [CfnAutoScalingPolicy(p) for p in self.asconn.get_all_policies()]
        context['scaling_policies'] = auto_scaling_policies
        return auto_scaling_policies

    def _form_sns_topics(self, context):
        topics = []
        for topic_arn in self.snsconn.get_all_topics()['ListTopicsResponse']['ListTopicsResult']['Topics']:
            subscriptions = self.snsconn.get_all_subscriptions_by_topic(topic_arn['TopicArn'])['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['Subscriptions']
            topics.extend([CfnSnsTopics(topic_arn, subscriptions)])
        context['sns_topics'] = topics
        return topics

    def _form_db_instance(self, context):
        db_instances = [CfnDBInstance(d) for d in self.rdsconn.get_all_dbinstances()]
        context['db_instances'] = db_instances
        return db_instances

    def _add_cfn_resource_map(self, context, cfn_objects):
        cfn_resource_map = context['cfn_resource_map'] if 'cfn_resource_map' in context else {}
        for cfn_object in cfn_objects:
            cfn_resource_map[cfn_object.id] = cfn_object.cfn_resource_name()
        context['cfn_resource_map'] = cfn_resource_map

