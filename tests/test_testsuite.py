from pprint import pprint

from tdl import TestSuite


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

    testsuite = TestSuite.load(data)
    # print(testsuite.__dict__)
    result = testsuite.run(env)
    pprint(result)


def test_test_suite2(env):
    data = {
        "name": "testsuite_01",
        "description": "testsuite description",
        "tags": ["api-test"],
        "priority": 1,
        "setups": [],
        "teardowns": [],
        "suite_steps": [],
        "suite_teardowns": [],
        "tests": [
            {
                "name": "test_api_demo_1",
                "description": "test description",
                "steps": [
                    {"name": "步骤1", "method": "Http.get",
                     "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}},
                    {"name": "步骤2", "method": "Http.post", "args": {"url": "/post", "json": {"name": "Kevin"}}},
                    {"name": "步骤3", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
                     "set": {"url": "$.url"}, "verify": [{"eq": ["$url", "/get"]}]}
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

    testsuite = TestSuite.load(data)
    # print(testsuite.__dict__)
    result = testsuite.run(env)
    print()
    pprint(result.data)
