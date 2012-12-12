# -*- coding:utf-8 -*-

import os
import sys
import argparse
from jinja2 import Environment, PackageLoader

from former import CloudFormer
import utils

def main():
# parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('vpcid')
    parser.add_argument('-O','--aws-access-key')
    parser.add_argument('-W','--aws-secret-key')
    parser.add_argument('--region')
    parsed = parser.parse_args()
    access_key, secret_key = utils.get_aws_key(parsed.aws_access_key, parsed.aws_secret_key)

# do form
    former = CloudFormer(vpc_id=parsed.vpcid, access_key=access_key, secret_key=secret_key, region_name=parsed.region)
    model = former.form()

# output
    env = Environment(loader=PackageLoader(__name__, 'templates'), trim_blocks='True')
    metatemplate = env.get_template('metatemplate.jinja2')
    print metatemplate.render(model=model);
