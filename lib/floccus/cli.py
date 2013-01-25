# -*- coding:utf-8 -*-

import os
import sys
import argparse

from floccus import Floccus
import utils
import dumper

def main():
# parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', default='us-east-1')
    parser.add_argument('-O','--aws-access-key', default=None)
    parser.add_argument('-W','--aws-secret-key', default=None)
    parsed = parser.parse_args()
    access_key, secret_key = utils.get_aws_key(parsed.aws_access_key, parsed.aws_secret_key)

# do form
    floccus = Floccus(access_key=access_key, secret_key=secret_key, region_name=parsed.region)
    model = floccus.form()

# output
    print dumper.output(model)
