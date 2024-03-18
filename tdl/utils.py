import functools
import logging
import signal
import uuid
from functools import reduce
from typing import Union


def gen_id():
    return str(uuid.uuid4()).replace('-', '')


def get_args_kwargs(args: Union[list, dict]):
    if isinstance(args, list):
        return args, {}
    if isinstance(args, dict):
        return [], args
    return [], {}


def do_dot(item, key: str):
    """单个content.url取值"""
    if hasattr(item, key):
        return getattr(item, key)
    if key.isdigit():
        key = int(key)
    try:
        return item[key]
    except Exception as ex:
        logging.exception(ex)
        return key


def get_field(data: dict, expr: str):
    """解析形如content.result.0.id的取值"""
    if '.' in expr:
        value = expr.split('.')
        field = data.get(value[0])
        return reduce(lambda x, y: do_dot(x, y), value[1:], field)
    else:
        return data.get(expr)


def with_timeout(seconds: int):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError(f'函数 {func.__name__} 运行超时 超时时间: {seconds}秒')

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)
            result = func(*args, **kwargs)
            signal.alarm(0)
            return result

        return wrapper

    return decorator
