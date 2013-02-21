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

def test_normalize_name():
    org = "sg-12e12123"
    result = normalize_name(org)
    expect = "sg12e12123"
    assert result == expect

def test_groupby_1():
    org = [
        { "ARN": "hoge", "Notification": "LAUNCH"},
        { "ARN": "hoge", "Notification": "ERROR"},
        { "ARN": "hoge", "Notification": "TERMINATE"},
        ]
    expect = [
        {"ARN": "hoge", "Notification" : ["LAUNCH", "ERROR", "TERMINATE"] }
        ]
    result = groupby(org, "ARN", "Notification")
    assert result == expect

def test_groupby_2():
    org = [
        { "ARN": "hoge", "Notification": "LAUNCH", "OTHER": "1"},
        { "ARN": "hoge", "Notification": "ERROR", "OTHER": "2"},
        { "ARN": "hoge", "Notification": "TERMINATE", "OTHER": "3"},
        ]
    expect = [
        {"ARN": "hoge", "Notification" : ["LAUNCH", "ERROR", "TERMINATE"] }
        ]
    result = groupby(org, "ARN", "Notification")
    assert result == expect

def test_groupby_3():
    org = [
        { "ARN": "hoge", "NRA": "LAUNCH"},
        { "ARN": "hoge", "NRA": "ERROR"},
        { "ARN": "hoge", "NRA": "TERMINATE"},
        ]
    expect = [
        {"ARN": "hoge", "NRA" : ["LAUNCH", "ERROR", "TERMINATE"] }
        ]
    result = groupby(org, "ARN", "NRA")
    assert result == expect

def test_groupby_3():
    org = [
        { "ARN": "hoge", "NRA": "LAUNCH"},
        { "ARN": "hoge", "NRA": "ERROR"},
        { "ARN": "hoge", "NRA": "TERMINATE"},
        { "ARN": "fuga", "NRA": "LAUNCH2"},
        { "ARN": "fuga", "NRA": "ERROR2"},
        { "ARN": "fuga", "NRA": "TERMINATE2"},
        ]
    expect = [
        {"ARN": "hoge", "NRA" : ["LAUNCH", "ERROR", "TERMINATE"] },
        {"ARN": "fuga", "NRA" : ["LAUNCH2", "ERROR2", "TERMINATE2"] }
        ]
    result = groupby(org, "ARN", "NRA")
    assert result == expect

def test_capitalize_dict():
    org = { "key": "keykey", "value": "valuevalue" }
    expect = { "Key": "keykey", "Value": "valuevalue" }
    result = capitalize_dict(org)
    assert result == expect
