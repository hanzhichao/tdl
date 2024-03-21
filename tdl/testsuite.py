import time
from typing import List

from . import Env, schema
from .context import Context
from .step import Step, StepStatus
from .testcase import TestCase, TestCaseStatus


class TestSuiteStatus:
    PASSED = 0
    FAILED = 1
    SETUP_ERROR = 5


class Filter(schema.Filter):
    def __init__(self, tests: List[TestCase], priorities: list = None, status: list = None,
                 tags: list = None, exclude_tags: list = None, exclude_names: list = None, **extra):
        self.tests = tests
        self.priorities = priorities
        self.status = status
        self.tags = tags
        self.exclude_tags = exclude_tags
        self.exclude_names = exclude_names
        self.extra = extra


class TestResult:
    def __init__(self, testsuite, env_info=None):
        self.testsuite_id = testsuite.id
        self.testsuite_name = testsuite.name
        self.env_info = env_info

        self.start_time = None
        self.end_time = None
        self.status = None
        self.error_msg = None

        self.total = 0
        self.passed = 0
        self.failed = 0
        self.error = 0
        self.skipped = 0

        self.pass_rate = None

        self.details = []

    def start(self):
        self.start_time = time.time()

    def end(self, status, error_msg=None):
        self.end_time = time.time()
        self.status = status
        if error_msg is not None:
            self.error_msg = error_msg
        if self.total > self.skipped:
            self.pass_rate = self.passed / (self.total - self.skipped)

    def add_testcase_result(self, testcase_result):
        testcase_status = testcase_result.status
        if testcase_status == TestCaseStatus.SKIPPED:
            self.skipped += 1
        elif testcase_status == TestCaseStatus.PASSED:
            self.passed += 1
        elif testcase_status == TestCaseStatus.FAILED:
            self.failed += 1
        else:
            self.error += 1
        self.total += 1
        self.details.append(testcase_result)

    @property
    def is_success(self):
        if self.status is not None:
            return self.status == TestSuiteStatus.PASSED

    @property
    def data(self):
        return dict(
            testsuite_id=self.testsuite_id,
            testsuite_name=self.testsuite_name,
            env_info=self.env_info,
            start_time=self.start_time,
            end_time=self.end_time,
            is_success=self.is_success,
            status=self.status,
            error_msg=self.error_msg,
            total=self.total,
            skipped=self.skipped,
            passed=self.passed,
            failed=self.failed,
            error=self.error,
            pass_rate=self.pass_rate,
            details=[item.data for item in self.details]
        )


class TestSuite(schema.TestSuite):

    def __init__(self, name: str, tests: List[dict], description: str = None, priority: int = None, status: int = None,
                 owner: str = None, tags: List[str] = None, timeout: int = None, setups: List[dict] = None,
                 teardowns: List[dict] = None, suite_setups: List[dict] = None,
                 suite_teardowns: List[dict] = None,
                 filter: dict = None, variables: dict = None, config: dict = None, **extra):
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
        self.variables = variables or {}

        self.config = config or {}

    @property
    def id(self):
        return ''

    def setup(self, context):
        for pre_step in self.suite_setups or []:
            result = pre_step.run(context)
            if result.status != StepStatus.PASSED:
                return result.error_msg

    def teardown(self, context):
        for post_step in self.suite_teardowns or []:
            post_step.run(context)

    def run(self, env: Env = None):
        env = env or Env()
        if self.config:
            env.config.update(self.config)
        if self.variables:
            env.variables.update(self.variables)

        context = env.context

        result = TestResult(self, env.info)
        result.start()
        error_msg = self.setup(context)
        if error_msg is not None:
            result.end(TestSuiteStatus.SETUP_ERROR, error_msg)
            return result
        status = TestSuiteStatus.PASSED
        for testcase in self.tests or []:
            testcase_results = testcase.run(env)
            for testcase_result in testcase_results:
                result.add_testcase_result(testcase_result)
                if status == TestSuiteStatus.PASSED and testcase_result.is_success is False:
                    status = TestSuiteStatus.FAILED
        result.end(status=status)
        self.teardown(context)
        return result

    @classmethod
    def load(cls, data: dict):
        return cls(**data)
