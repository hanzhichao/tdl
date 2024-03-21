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


class StepState:
    SETUP = 0
    TEST = 1
    VERIFY = 2
    TEARDOWN = 3


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


def parse_step(data: str) -> dict:
    method, *raw_args = data.split(' ')
    args, kwargs = [], {}
    for item in raw_args:
        if item.strip():
            if '=' in item:
                key, value = item.split('=', 1)
                if value.startswith("{") or value.startswith("["):
                    value = eval(value)
                kwargs[key] = value
            else:
                args.append(item)
    return {
        'method': method,
        'args': args,
        'kwargs': kwargs,
    }


class Step(schema.Step):
    def __init__(self, method: str, args: Union[list, dict] = None, kwargs: dict = None, name: str = None,
                 order: int = None, state: int = StepState.TEST,
                 timeout: int = None, store: dict = None,
                 verify: dict = None, skip=None, **extra):
        self.method = method
        # self.args = args
        self.name = name or method
        self.timeout = timeout
        self.store = store
        self.verify = verify
        self.skip = skip

        self.order = order
        self.state = state

        self.extra = extra

        self.args, self.kwargs = get_args_kwargs(args, kwargs)

        if self.timeout is not None:
            assert isinstance(self.timeout, int) and self.timeout > 0, '仅支持timeout为正整数'


    @property
    def id(self):
        return ''

    def _get_method(self, context: Context, method_expr: str):
        if '.' in method_expr:
            library_name, method_name = method_expr.split('.', 1)
        else:
            library_name, method_name = 'Default', method_expr

        library_instance = context.get_library(library_name)
        method = getattr(library_instance, method_name)
        if hasattr(library_instance, 'NO_STORE_RESULT'):
            setattr(self, 'NO_STORE_RESULT', True)

        return method

    def _call_method(self, context: Context):
        method = self._get_method(context, self.method)
        # 解析参数中的$变量引用
        args = [context.get_variable(item) for item in self.args]
        kwargs = {key: context.get_variable(value) for key, value in self.kwargs.items() if isinstance(value, str)}

        result = method(*args, **kwargs)
        if not hasattr(self, 'NO_STORE_RESULT'):
            context.set_variable('result', result)

        if self.state == StepState.TEST:
            prefix = 'step'
        elif self.state == StepState.SETUP:
            prefix = 'setup'
        elif self.state == StepState.TEARDOWN:
            prefix = 'teardown'
        else:
            raise Exception('不支持改步骤类型')

        context.set_variable('%s%d' % (prefix, self.order), result)

        return result

    def call_method(self, context: Context):
        if self.timeout is not None and isinstance(self.timeout, int):
            return with_timeout(self.timeout)(self._call_method)(context)
        return self._call_method(context)

    def set_variables(self, context):
        if self.store:
            for key, value in self.store.items():
                context.set_variable(key, value)

    def verify_results(self, context):
        if self.verify:
            for item in self.verify:
                context.verify(item)

    def run(self, context: Context = None) -> StepResult:
        context = context or None
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

        return step_result

    @classmethod
    def load(cls, data: Union[dict, str], index: int = None, state: int = None):
        if isinstance(data, str):
            data = parse_step(data)
        data['order'] = index + 1
        data['state'] = state
        return cls(**data)
