from pprint import pprint

import pytest

from tdl import main


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
