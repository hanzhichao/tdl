import time
import traceback
import uuid
from typing import List, Union

from . import models
from .context import Context
# from .libs import Default, Http

# _ = Default, Http


def gen_id():
    return str(uuid.uuid4()).replace('-', '')

class Env:
    def __init__(self, name: str, description: str = None, config: dict = None, variables: dict = None):
        self.name = name
        self.description = description
        self.config = config
        self.variables = variables

        self.context = Context(config=config, variables=variables)

    @classmethod
    def load(cls, data: dict):
        return cls(**data)


class Step(models.Step):
    def __init__(self, method: str, args: Union[list, dict] = None, name: str = None, register: dict = None,
                 excepted: dict = None, **extra):
        self.method = method
        self.args = args if isinstance(args, list) else []
        self.kwargs = args if isinstance(args, dict) else {}
        self.name = name or method
        self.register = register
        self.excepted = excepted
        self.extra = extra

        self.result = {'id':self.id, 'name': self.name}

    @property
    def id(self):
        return gen_id()


    def run(self, context: Context = None):
        self.result['start_time'] = time.time()
        try:
            context = context or Context()
            method = context.get_method(self.method)
            args = [context.get(item) for item in self.args]
            kwargs = {key: context.get(value) for key, value in self.kwargs.items()}
            result = method(*args, **kwargs)
            # result = method(*self.args, **self.kwargs)
        except Exception as ex:
            self.result['is_success'] = False
            self.result['error_info'] = traceback.format_exc()
            self.result['result'] = None
            context.set('result', None)
        else:
            self.result['is_success'] = True
            self.result['result'] = result
            self.result['error_info'] = None
            # print(self.method, '->', result)
            context.set('result', result)
        finally:
            self.result['end_time'] = time.time()

        return self.result

    @classmethod
    def load(cls, data: dict):
        return cls(**data)


class TestCase(models.TestCase):
    def __init__(self, name: str, steps: List[dict], description: str = None, priority: int = None, status: int = None,
                 owner: str = None, tags: List[str] = None, timeout: int = None, setups: List[dict] = None,
                 teardowns: List[dict] = None, defaults: dict=None, **extra):
        defaults = defaults or {}
        setups = setups or defaults.get('setups')
        teardowns = teardowns or defaults.get('teardowns')
        self.name = name
        self.steps = [Step(**item) for item in steps]
        self.description = description
        self.priority = priority or defaults.get('priority')
        self.status = status or defaults.get('status')
        self.owner = owner or defaults.get('owner')
        self.tags = tags or defaults.get('tags')
        self.timeout = timeout or defaults.get('tags')
        self.setups = [Step(**item) for item in setups] if setups else None
        self.teardowns = [Step(**item) for item in teardowns] if teardowns else None
        self.extra = extra

        self.result = {'id':self.id, 'name': self.name}

    def run(self, env: Env = None):
        self.result['start_time'] = time.time()
        self.result['details'] = []
        context = env.context if env else Context()
        is_success = True
        try:
            for pre_step in self.setups or []:
                pre_step.run(context)  # todo record details
        except Exception as ex:
            self.result['is_success'] = False
            self.result['error_info'] = traceback.format_exc()
        else:
            try:
                for test_step in self.steps or []:
                    step_result = test_step.run(context)
                    if step_result.get('is_success') is False:
                        is_success = False
                    self.result['details'].append(step_result)
            except Exception as ex:
                self.result['is_success'] = False
                self.result['error_info'] = traceback.format_exc()
            else:
                self.result['is_success'] = is_success
            finally:
                try:
                    for post_step in self.teardowns or []:  # todo record details
                        post_step.run(context)
                except Exception as ex:
                    raise
        finally:
            self.result['end_time'] = time.time()

        return self.result

    @property
    def id(self):
        return gen_id()

    @classmethod
    def load(cls, data: dict):
        return cls(**data)

class Filter(models.Filter):
    def __init__(self, tests: List[TestCase], priorities: list=None, status: list=None,
                 tags: list=None, exclude_tags: list=None, exclude_names: list=None, **extra):
        self.tests = tests
        self.priorities = priorities
        self.status = status
        self.tags = tags
        self.exclude_tags = exclude_tags
        self.exclude_names = exclude_names
        self.extra = extra


class TestResult(models.TestResult):
    pass


class TestSuite(models.TestSuite):

    def __init__(self, name: str, tests: List[dict], description: str = None, priority: int = None, status: int = None,
                 owner: str = None, tags: List[str] = None, timeout: int = None, setups: List[dict] = None,
                 teardowns: List[dict] = None, suite_setups: List[dict]=None,
                 suite_teardowns: List[dict] = None,
                 filter: dict = None, **extra):
        self.name = name
        defaults = dict(priority=priority,
                        status=status,
                        owner=owner,
                        tags=tags,
                        timeout=timeout,
                        setups=setups,
                        teardowns=teardowns
                        )
        self.tests = [TestCase(**item, defaults=defaults) for item in tests]
        self.description = description

        self.suite_setups = [Step(**item) for item in setups] if suite_setups else None
        self.suite_teardowns = [Step(**item) for item in teardowns] if suite_teardowns else None
        filter = filter or {}
        self.filter = Filter(tests=self.tests, **filter)
        self.extra = extra

        self.result = {'id':self.id, 'name': self.name}

    @property
    def id(self):
        return gen_id()


    def run(self, env=None):
        self.result['start_time'] = time.time()
        self.result['details'] = []
        context = env.context if env else Context()
        try:
            for pre_step in self.suite_setups or []:
                pre_step.run(context)
        except Exception as ex:
            self.result['is_success'] = False
            self.result['error_info'] = traceback.format_exc()
            raise
        else:
            try:
                for testcase in self.tests or []:
                    testcase_result = testcase.run(env)
                    self.result['details'].append(testcase_result)
            except Exception as ex:
                self.result['is_success'] = False
                self.result['error_info'] = traceback.format_exc()
                raise
            finally:
                try:
                    for post_step in self.suite_teardowns or []:
                        post_step.run(context)
                except Exception as ex:
                    raise
        finally:
            self.result['end_time'] = time.time()

        return self.result


    @classmethod
    def load(cls, data: dict):
        return cls(**data)
