# -*- coding:utf-8 -*-

from floccus.utils import *
import json

def test_flatten_1():
    org = {
        'aaa':'value_of_aaa',
        'bbb': [{'bbb1':'value_of_bbb1'},
                  {'bbb2':'value_of_bbb2'}],
        'ccc':'value_of_ccc'
        }
    result = flatten(org,'bbb')
    expect = [
        {
            'aaa':'value_of_aaa',
            'bbb1':'value_of_bbb1',
            'ccc':'value_of_ccc'
            },
        {
            'aaa':'value_of_aaa',
            'bbb2':'value_of_bbb2',
            'ccc':'value_of_ccc'
            },
        ]

    assert result == expect

def test_flatten_2():
    org = {
        'aaa':'value_of_aaa',
        'bbb': [{'bbb1':'value_of_bbb1'}],
        'ccc':'value_of_ccc'
        }
    result = flatten(org,'bbb')
    expect = [
        {
            'aaa':'value_of_aaa',
            'bbb1':'value_of_bbb1',
            'ccc':'value_of_ccc'
            },
        ]
    assert result == expect
