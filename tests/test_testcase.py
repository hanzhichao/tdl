from tdl import TestCase
from tdl.testcase import TestCaseStatus


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
             "set": {"url": "$result.url"}, "verify": [{"eq": ["$url", "/get"]}]}
        ]
    }
    testcase = TestCase.load(data)
    result = testcase.run(env)
    assert result[0].status == TestCaseStatus.PASSED


def test_testcase_with_assertion_step(env):
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
    testcase = TestCase.load(data)
    result = testcase.run(env)
    assert result[0].status == TestCaseStatus.PASSED


def test_testcase_from_fasttest(env):
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
    testcase = TestCase.load(data)
    result = testcase.run(env)
    assert result[0].status == TestCaseStatus.PASSED


