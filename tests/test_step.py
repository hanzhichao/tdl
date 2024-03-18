import re
from pprint import pprint

from tdl import Step
from tdl.step import StepStatus


def test_step(context):
    data = {"method": "Http.get",
            "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}}

    step = Step.load(data)
    result = step.run(context)
    assert result.status == StepStatus.PASSED


def test_step_with_set_verify(context):
    data = {"method": "Http.get",
            "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
            "set": {"url": "$result.url"},
            "verify": [
                {"eq": ["$result.status_code", 200]},
                {"eq": ["$url", "http://postman-echo.com/get?a=1&b=2&c=3"]},
                {"contains": ["$result.url", "http://postman-echo.com/get"]},

            ]}
    step = Step.load(data)
    result = step.run(context)
    pprint(result.data)
    assert result.status == StepStatus.PASSED


def test_step_skip(context):
    data = {
        "method": "Http.get",
        "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
        "skip": [2 > 1, '跳过吧']
    }
    step = Step.load(data)
    result = step.run(context)
    assert result.status == StepStatus.SKIPPED


def test_step_timeout(context):
    data = {
        "timeout": 1,
        "method": "sleep",
        "args": [5],
    }
    step = Step.load(data)
    result = step.run(context)
    pprint(result.data)
    assert result.status == StepStatus.TIMEOUT


def test_one_line_step(context):
    data = 'Http.get /get  params={"a":1,"b":2,"c":3}'
    step = Step.load(data)
    result = step.run(context)
    pprint(result.data)
    assert result.status == StepStatus.PASSED
