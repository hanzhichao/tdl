import time
import traceback
from typing import Union

from . import schema
from .context import Context
from .utils import get_args_kwargs, with_timeout


class StepStatus:
    PASSED = 0
    FAILED = 1
    ERROR = 2
    SKIPPED = 3
    TIMEOUT = 4


class StepResult:
    def __init__(self, step):
        self.step_id = step.id
        self.step_name = step.name
        self.start_time = None
        self.end_time = None
        self.result = None
        self.error_msg = None
        self.status = None  # 0 passed, 1 failed, 2 error, 3 skipped

    @property
    def is_success(self):
        if self.status is not None:
            return self.status == StepStatus.PASSED

    @property
    def data(self):
        return dict(
            step_id=self.step_id,
            step_name=self.step_name,
            start_time=self.start_time,
            end_time=self.end_time,
            is_success=self.is_success,
            status=self.status,
            result=self.result,
            error_msg=self.error_msg,
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


class Step(schema.Step):
    def __init__(self, method: str, args: Union[list, dict] = None, name: str = None,
                 timeout: int = None, set: dict = None,
                 verify: dict = None, skip=None, **extra):
        self.method = method
        self.args = args
        self.name = name or method
        self.timeout = timeout
        self.set = set
        self.verify = verify
        self.skip = skip
        self.extra = extra


    @property
    def id(self):
        return ''

    def _call_method(self, context: Context = None):
        context = context or Context()
        method = context.get_method(self.method)
        args, kwargs = get_args_kwargs(self.args)
        return method(*args, **kwargs)

    def call_method(self, context: Context = None):
        if self.timeout is not None and isinstance(self.timeout, int):
            return with_timeout(self.timeout)(self._call_method)(context)
        return self._call_method(context)

    def set_variables(self, context):
        if self.set:
            for key, value in self.set.items():
                context.set_variable(key, value)

    def verify_results(self, context):
        if self.verify:
            for item in self.verify:
                context.verify(item)

    def run(self, context: Context = None) -> StepResult:
        step_result = StepResult(step=self)
        step_result.start()

        skip, reason = context.skip_check(self.skip)
        if skip:
            step_result.end(status=StepStatus.SKIPPED, error_msg=reason)
            return step_result

        try:
            result = self.call_method(context)
        except AssertionError:
            step_result.end(status=StepStatus.FAILED, error_msg=traceback.format_exc())
        except TimeoutError:
            step_result.end(status=StepStatus.TIMEOUT, error_msg=traceback.format_exc())
        except Exception:
            step_result.end(status=StepStatus.TIMEOUT, error_msg=traceback.format_exc())
        else:
            step_result.end(status=StepStatus.PASSED, result=result)
            context.set_variable('result', result)
        return step_result

    @classmethod
    def load(cls, data: dict):
        return cls(**data)
