# -*- coding:utf-8 -*-

from jinja2 import Environment, PackageLoader

import sys

sys.path.insert(0, '..')

env = Environment(loader=PackageLoader(__name__, 'metatemplate'))
metatemplate = env.get_template('metatemplate.jinja2')

template = {
    'version':'2010-09-10',
    'description':'hello',
    'parameters': [
        {'name': 'aaa'},
        {'name': 'bbb'},
    ],
    'mappings': [
        {'key': 'key1', 'value': 'value1'},
    ],
    'resources': {
        'resource_1': {
            'Type': '',
            'Properties': {
                }
            },
        'resource_2': {
            'Type': '',
            'Properties': {
                }
            }
    },
    'outputs': [
    ],
}

print metatemplate.render(template=template);
