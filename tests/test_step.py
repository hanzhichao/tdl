from pprint import pprint

from tdl import Step


def test_step(context):
    data = {"method": "Http.get",
            "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}}

    step = Step.load(data)
    pprint(step.__dict__)
    result = step.run(context)
    pprint(result)


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
    print('\nStep --------------------------------')
    pprint(step.__dict__)
    result = step.run(context)
    print('\nContext --------------------------------')
    pprint(context.variables)
    print('\nResult --------------------------------')
    pprint(result.data)


def test_step_skip(context):
    data = {"method": "Http.get",
            "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
            "skip": [2 > 1, '跳过吧']
            }
    step = Step.load(data)
    print('\nStep --------------------------------')
    pprint(step.__dict__)
    result = step.run(context)
    print('\nContext --------------------------------')
    pprint(context.variables)
    print('\nResult --------------------------------')
    pprint(result.data)
