# -*- coding:utf-8 -*-

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader(__name__, 'templates'))
metatemplate = env.get_template('metatemplate.jinja2')

template = {
    'description':'hello',
    'parameters': [
        {'name': 'aaa'},
    ],
    'mappings': [
        {'key': 'key1', 'value': 'value1'},
    ],
    'resources': [
    ],
    'outputs': [
    ],
}


print metatemplate.render(template=template);
