# -*- coding:utf-8 -*-

import os
import sys
import json
import argparse

import floccus.former
import floccus.dumper
from floccus.models import load_exclude_pattern

def main():
    parser = argparse.ArgumentParser(description='Outputs cloudFormation template json.')
    parser.add_argument('--region', dest='region', action='store', default='us-east-1', help='target AWS region. (default:us-east-1)')
    parser.add_argument('--exclude-from', dest='exclude_from', action='store', default=None, help='do not output pattern from file.')
    args = parser.parse_args()

# prepare exclude pattern
    if args.exclude_from is not None:
        load_exclude_pattern(args.exclude_from)

# do form
    former = floccus.former.Former(region=args.region)
    model = former.form()

# output
    print floccus.dumper.output(model)
