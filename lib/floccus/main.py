import os
import sys
import argparse

from jinja2 import Environment, PackageLoader
from loader import CloudFormer

parser = argparse.ArgumentParser()
parser.add_argument('vpcid')
parser.add_argument('-O','--aws-access-key')
parser.add_argument('-W','--aws-secret-key')
parsed = parser.parse_args()
access_key = parsed.aws_access_key if parsed.aws_access_key is not None else os.environ.get('AWS_ACCESS_KEY')
secret_key = parsed.aws_secret_key if parsed.aws_secret_key is not None else os.environ.get('AWS_SECRET_KEY')
former = CloudFormer(vpc_id=parsed.vpcid, access_key=access_key, secret_key=secret_key)
env = Environment(loader=PackageLoader(__name__, 'templates'), trim_blocks='True')
metatemplate = env.get_template('metatemplate.jinja2')
model = former.form()
print metatemplate.render(model=model);
