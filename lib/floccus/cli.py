# -*- coding:utf-8 -*-

import os
import sys

import floccus.former
import floccus.dumper

def main():
# do form
    former = floccus.former.Former()
    model = former.form()

# output
    print floccus.dumper.output(model)
