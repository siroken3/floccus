# -*- coding:utf-8 -*-

import os

def get_aws_key(access_key=None, secret_key=None):
    if access_key is None:
        if os.environ.get('AWS_ACCESS_KEY') is None:
            aws_access_key = ''
        else:
            aws_access_key = os.environ.get('AWS_ACCESS_KEY')
    else:
        aws_access_key = access_key

    if secret_key is None:
        if os.environ.get('AWS_SECRET_KEY') is None:
            aws_secret_key = ''
        else:
            aws_secret_key = os.environ.get('AWS_SECRET_KEY')
    else:
        aws_secret_key = secret_key

    return (aws_access_key, aws_secret_key)
