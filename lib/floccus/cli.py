# -*- coding:utf-8 -*-

import os
import sys
import json
import argparse
import ConfigParser

import floccus.former
import floccus.dumper
from floccus.models import load_exclude_pattern

config = ConfigParser.SafeConfigParser()

def main():
    parser = argparse.ArgumentParser(description='Outputs cloudFormation template json.')
    parser.add_argument('--region', dest='region', action='store', default='us-east-1', help='target AWS region. (default:us-east-1)')
    parser.add_argument('--config', dest='config', action='store', default='flcs.conf', help='configuration for output json files (default: flcs.conf)')
    args = parser.parse_args()

# prepare exclude pattern
    if args.config is not None:
        config.readfp(open(args.config))

# do form
    for section in config.sections():
        load_exclude_pattern(config.get(section, 'exclude_from'))
        former = floccus.former.Former(region=args.region)
        model = former.form()

# output
        outfile = config.get(section, 'outfile')
        floccus.dumper.output(model, outfile=outfile)
