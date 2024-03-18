import copy
import time
import traceback
from typing import List, Union

from . import schema
from .context import Context
from .env import Env
from .step import Step, StepStatus
from .utils import with_timeout

DEFAULT_RETRY_INTERVAL = 1


def parse_retry(retry: Union[int, List[int]]):
    if isinstance(retry, list) and len(retry) > 1:
        retry_limit, retry_interval, *_ = retry
    elif isinstance(retry, int):
        retry_limit, retry_interval = retry, DEFAULT_RETRY_INTERVAL
    else:
        retry_limit, retry_interval = None, None
    return retry_limit, retry_interval


class TestCaseStatus:
    PASSED = 0
    FAILED = 1
    ERROR = 2
    SKIPPED = 3
    TIMEOUT = 4
    SETUP_ERROR = 5


class TestRecord:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.result = None
        self.error_msg = None
        self.status = None

        self.details = []

    @property
    def is_success(self):
        if self.status is not None:
            return self.status == TestCaseStatus.PASSED

    def add_step_result(self, step_result):
        self.details.append(step_result)

    @property
    def data(self):
        return dict(
            start_time=self.start_time,
            end_time=self.end_time,
            is_success=self.is_success,
            status=self.status,
            result=self.result,
            error_msg=self.error_msg,
            details=[item.data for item in self.details]
        )

    def start(self):
        self.start_time = time.time()

    def end(self, status, result=None, error_msg=None):
        self.end_time = time.time()
        self.status = status
        if result is not None:
            self.result = result
        if error_msg is not None:
            self.error_msg = error_msg


class TestCaseResult:
    def __init__(self, testcase):
        self.testcase_id = testcase.id
        self.testcase_name = testcase.name
        self.start_time = None
        self.end_time = None
        self.error_msg = None
        self.status = None
        self.records = []

    @property
    def is_success(self):
        if self.status is not None:
            return self.status == TestCaseStatus.PASSED

    def start(self):
        self.start_time = time.time()

    def end(self, status, result=None, error_msg=None):
        self.end_time = time.time()
        self.status = status
        self.error_msg = error_msg

    def add_record(self, record):
        self.records.append(record)

    @property
    def data(self):
        return dict(
            testcase_id=self.testcase_id,
            testcase_name=self.testcase_name,
            start_time=self.start_time,
            end_time=self.end_time,
            is_success=self.is_success,
            status=self.status,
            error_msg=self.error_msg,
            records=[item.data for item in self.records]
        )


class TestCase(schema.TestCase):
    def __init__(self, name: str, steps: List[dict], description: str = None, priority: int = None, status: int = None,
                 owner: str = None, tags: List[str] = None,
                 timeout: int = None, retry: List[int] = None,
                 setups: List[dict] = None,
                 teardowns: List[dict] = None, defaults: dict = None, skip=None,
                 variables=None, data=None, **extra):
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
        self.timeout = timeout or defaults.get('timeout')
        self.setups = [Step(**item) for item in setups] if setups else None
        self.teardowns = [Step(**item) for item in teardowns] if teardowns else None
        self.retry_limit, self.retry_interval = parse_retry(retry)
        self.data = data
        self.variables = variables or defaults.get('variables') or {}

        self.skip = skip or defaults.get('skip')

        self.extra = extra

    def setup(self, context):
        for pre_step in self.setups or []:
            result = pre_step.run(context)
            if result.status != StepStatus.PASSED:
                return result.error_msg

    def teardown(self, context):
        for post_step in self.teardowns or []:
            post_step.run(context)

    def _run(self, test_record, env: Env = None) -> TestRecord:
        context = env.context if env else Context()

        context.variables.update(self.variables)

        skip, reason = context.skip_check(self.skip)
        if skip:
            test_record.end(status=TestCaseStatus.SKIPPED, error_msg=reason)
            return test_record

        error_msg = self.setup(context)
        if error_msg is not None:
            test_record.end(status=TestCaseStatus.SETUP_ERROR, error_msg=error_msg)
            return test_record

        for test_step in self.steps or []:
            step_result = test_step.run(context)
            test_record.add_step_result(step_result)

            if step_result.status == StepStatus.PASSED:
                test_record.end(status=TestCaseStatus.PASSED)
            else:
                status = TestCaseStatus.FAILED if step_result.status == StepStatus.FAILED else TestCaseStatus.ERROR
                test_record.end(status=status, error_msg=step_result.error_msg)
                break

        self.teardown(context)

        return test_record

    def _run_with_timeout(self, env) -> TestRecord:
        test_record = TestRecord()
        test_record.start()
        if self.timeout is not None and isinstance(self.timeout, int):
            try:
                return with_timeout(self.timeout)(self._run)(test_record, env)
            except TimeoutError:
                test_record.end(status=TestCaseStatus.TIMEOUT, error_msg=traceback.format_exc())
                return test_record
        return self._run(test_record, env)

    def _run_with_timeout_and_retry(self, env) -> TestCaseResult:
        testcase_result = TestCaseResult(self)
        run_count = (self.retry_limit or 0) + 1
        interval = self.retry_interval or DEFAULT_RETRY_INTERVAL
        testcase_result.start()
        record = None
        for i in range(run_count):
            record = self._run_with_timeout(env)
            testcase_result.add_record(record)
            if record.is_success:
                testcase_result.end(status=TestCaseStatus.PASSED)
                break
            if i < run_count - 1:
                time.sleep(interval)
        else:
            if record is not None:
                testcase_result.end(status=record.status, error_msg=record.error_msg)
            else:
                testcase_result.end(status=None)
        return testcase_result

    def _run_with_data_timeout_and_retry(self, env=None) -> List[TestCaseResult]:
        results = []
        for item in self.data:
            testcase = copy.copy(self)
            testcase.variables.update(item)
            subfix = '-'.join(map(str, item.values()))
            testcase.name = f'{self.name}-{subfix}'
            testcase.description = f'{self.description}-{subfix}'
            results.append(testcase._run_with_timeout_and_retry(env))
        return results

    def run(self, env: Env = None) -> List[TestCaseResult]:
        if self.data is not None:
            return self._run_with_data_timeout_and_retry(env)
        return [self._run_with_timeout_and_retry(env)]

    @property
    def id(self):
        return ''

    @classmethod
    def load(cls, data: dict):
        return cls(**data)
