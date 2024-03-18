import abc
from typing import Callable, Dict, List, Optional, Union


class Context:
    libraries: dict
    variables: Optional[dict]
    config: Optional[dict]

    def get(self):
        pass

    def set(self):
        pass

    def get_method(self, method: str)->Callable:
        pass

    @classmethod
    def register_library(cls, *args, **kwargs):
        pass


class Env:
    name: str
    config: Optional[dict]
    variables: Optional[dict]

    context: Context

    @abc.abstractmethod
    def info(self):
        pass


class StepOptionMixIn:
    excepted: Optional[List[dict]]
    register: Optional[Dict[str, str]]


class Step(StepOptionMixIn, metaclass=abc.ABCMeta):
    method: str
    args: Optional[Union[list, dict]]
    name: Optional[str]

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Step %s>' % self.method

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    @abc.abstractmethod
    def run(self, context: Context=None):
        pass


class FilterOptionsMixIn:
    priority: Optional[int]
    status: Optional[int]
    owner: Optional[str]
    tags: Optional[List[str]]


class RunnerOptionsMixIn:
    timeout: Optional[int]


class BaseTest(FilterOptionsMixIn, RunnerOptionsMixIn, metaclass=abc.ABCMeta):
    name: str
    description: Optional[str]
    setups: Optional[List[Step]]
    teardowns: Optional[List[Step]]


class TestCase(BaseTest):
    steps: List[Step]

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<TestCase %s>' % self

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    @abc.abstractmethod
    def id(self) -> int:
        pass

    @abc.abstractmethod
    def run(self, env: Env = None):
        pass


class Filter:
    tests: List[TestCase]

    priorities: Optional[List[int]]
    status: Optional[List[int]]
    tags: Optional[List[str]]
    exclude_tags: Optional[List[str]]
    exclude_names: Optional[List[str]]


class TestSuite(BaseTest):
    tests: List[TestCase]
    suite_setups: Optional[List[Step]]
    suite_teardowns: Optional[List[Step]]
    filter: Optional[Filter]

    @abc.abstractmethod
    def id(self) -> int:
        pass


class Summary:
    start_time: str
    end_time: str
    total: int
    run: int
    passed: int
    failed: int
    is_success: bool

    title: Optional[str]
    env: Optional[dict]


class BaseRecord:
    start_time: str
    end_time: str
    error_info: Optional[str]
    is_success: bool


class StepRecord(BaseRecord):
    step: Step


class TestCaseRecord(BaseRecord):
    details: List[StepRecord]


class TestCaseResult(BaseRecord):
    testcase: TestCase
    records: List[TestCaseRecord]


class TestResult(metaclass=abc.ABCMeta):
    summary: Summary

    description: Optional[str]
    details: List[TestCaseResult]
