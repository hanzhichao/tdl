from pprint import pprint

import pytest

import tests.libs
from tdl import main

libs = tests.libs

@pytest.fixture
def env():
    env = main.Env('test', config={'Http': {'base_url': 'http://postman-echo.com'}})
    return env


@pytest.fixture
def context(env):
    return env.context


def test_step(context):
    data = {"method": "Http.get",
            "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}}

    step = main.Step.load(data)
    pprint(step.__dict__)
    result = step.run(context)
    pprint(result)


def test_testcase(env):
    data = {
        "name": "test_api_demo",
        "description": "test description",
        "priority": 1,
        "tags": ["http", "api-test"],
        "timeout": 100,
        "setups": [
            {"name": "测试准备", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}}
        ],
        "teardowns": [
            {"name": "测试清理", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}}
        ],
        "steps": [
            {"name": "步骤1", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}},
            {"name": "步骤2", "method": "Http.post", "args": {"url": "/post", "json": {"name": "Kevin"}}},
            {"name": "步骤3", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
             "register": {"url": "$.url"}, "excepted": [{"eq": ["$url", "/get"]}]}
        ]
    }
    testcase = main.TestCase.load(data)
    pprint(testcase.__dict__)
    result = testcase.run(env)
    pprint(result)


def test_testcase2(env):
    print(env.context.libraries)
    data = {'description': '示例接口测试用例1',
            'name': '用例1',
            'priority': 2,
            'setups': [{'args': {'url': '/get?type=setup'},
                        'method': 'Http.get',
                        'name': '准备步骤1'},
                       {'args': {'url': '/get?type=setup'},
                        'method': 'Http.get',
                        'name': '准备步骤2'}],
            'steps': [{'args': {'url': '/get?type=test'},
                       'method': 'Http.get',
                       'name': '步骤1'},
                      {'args': {'url': '/post?type=test'},
                       'method': 'Http.post',
                       'name': '步骤2'},
                      {'args': {'url': '/post?type=test'},
                       'method': 'Http.post',
                       'name': '步骤3'},
                      {'args': ['$result.url', '/post'],
                       'method': 'Assert.contains',
                       'name': '断言'}],
            'tags': ['示例', '接口测试', '功能测试'],
            'teardowns': [{'args': {'url': '/get?type=setup'},
                           'method': 'Http.get',
                           'name': '清理步骤1'}]}
    testcase = main.TestCase.load(data)
    pprint(testcase.__dict__)
    result = testcase.run(env)
    pprint(result)


def test_test_suite(env):
    data = {
        "name": "testsuite_01",
        "description": "testsuite description",
        "tags": ["api-test"],
        "priority": 1,
        "setups": [],
        "teardowns": [],
        "suite_steps": [],
        "suite_teardown": [],
        "tests": [
            {
                "name": "test_api_demo_1",
                "description": "test description",
                "steps": [
                    {"name": "步骤1", "method": "Http.get",
                     "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}},
                    {"name": "步骤2", "method": "Http.post", "args": {"url": "/post", "json": {"name": "Kevin"}}},
                    {"name": "步骤3", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
                     "register": {"url": "$.url"}, "excepted": [{"eq": ["$url", "/get"]}]}
                ]
            },
            {
                "name": "test_api_demo_2",
                "description": "test description",
                "steps": [
                    {"name": "步骤1", "method": "Http.get",
                     "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}},
                    {"name": "步骤2", "method": "Http.post", "args": {"url": "/post", "json": {"name": "Kevin"}}},
                ]
            }
        ]
    }

    testsuite = main.TestSuite.load(data)
    # print(testsuite.__dict__)
    result = testsuite.run(env)
    pprint(result)
