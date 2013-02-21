# -*- coding:utf-8 -*-

import os
import sys
import argparse

import floccus.former
import floccus.dumper

def main():
    parser = argparse.ArgumentParser(description='Outputs cloudFormation template json.')
    parser.add_argument('--region', dest='region', action='store', default='us-east-1', help='target AWS region. (default:us-east-1)')
    args = parser.parse_args()

# do form
    former = floccus.former.Former(region=args.region)
    model = former.form()

# output
    print floccus.dumper.output(model)
