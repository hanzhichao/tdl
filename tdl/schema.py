import abc
from typing import Callable, Dict, List, Optional, Tuple, Union


class SchemaKey:
    STEP_SET = 'set'
    STEP_VERIFY = 'verify'

    TESTSUITE_TESTS = 'tests'


class TestStatus:
    PASSED = 0
    FAILED = 1
    ERROR = 2
    SKIPPED = 3
    XPASSED = 4
    XFAILED = 5


class Context(metaclass=abc.ABCMeta):
    libraries: dict
    variables: Optional[dict]
    config: Optional[dict]

    def get(self):
        pass

    def set(self):
        pass

    @abc.abstractmethod
    def get_method(self, method: str) -> Callable:
        pass

    @abc.abstractmethod
    def register_library(cls, *args, **kwargs):
        pass


class Env:
    name: str
    config: Optional[dict]
    variables: Optional[dict]

    @abc.abstractmethod
    def context(self) -> Context:
        pass

    @abc.abstractmethod
    def info(self) -> dict:
        return {'name': self.name, 'config': self.config}


class Step(metaclass=abc.ABCMeta):
    method: str
    args: Optional[Union[list, dict]]
    name: Optional[str]

    verify: Optional[List[dict]]
    set: Optional[Dict[str, str]]

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Step %s>' % self.method

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    @abc.abstractmethod
    def id(self):
        pass

    @abc.abstractmethod
    def run(self, context: Context = None):
        pass



class TestCase:
    name: str
    description: Optional[str]

    priority: Optional[int]
    status: Optional[int]
    owner: Optional[str]
    tags: Optional[List[str]]
    timeout: Optional[int]

    data: Optional[List[dict]]
    data_file: Optional[str]

    skip: Optional[Union[bool, str, list]]

    steps: List[Step]
    setups: Optional[List[Step]]
    teardowns: Optional[List[Step]]

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


class TestSuite:
    name: str
    description: Optional[str]
    priority: Optional[int]
    status: Optional[int]
    owner: Optional[str]
    tags: Optional[List[str]]
    timeout: Optional[int]
    setups: Optional[List[Step]]
    teardowns: Optional[List[Step]]

    tests: List[TestCase]
    suite_setups: Optional[List[Step]]
    suite_teardowns: Optional[List[Step]]
    filter: Optional[Filter]

    @abc.abstractmethod
    def id(self) -> int:
        pass


class BaseResult:
    start_time: Optional[float]
    end_time: Optional[float]
    is_success: Optional[bool]
    status: Optional[int]
    error_msg: Optional[str]


class StepResult(BaseResult):
    step_id: Union[int, str]
    step_name: str


class TestCaseRecord(BaseResult):
    details: List[StepResult]


class TestCaseResult(BaseResult):
    testcase_id: Union[int, str]
    testcase_name: str
    records: List[TestCaseRecord]


class TestResult(BaseResult):
    title: Optional[str]
    description: Optional[str]

    testsuite_id: Union[int, str]
    testsuite_name: str
    env: Optional[dict]
    total: int
    passed: int
    failed: int
    details: List[TestCaseResult]
