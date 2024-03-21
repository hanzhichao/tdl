import operator
import os
import re
from collections import ChainMap
from typing import Optional, Union

from .utils import get_args_kwargs, get_field

DOLLAR_VARIABLE = re.compile('\${?([\w.]+)}?')
PURE_DOLLAR_VARIABLE = re.compile('^\${?([\w.]+)}?$')

ASSERT_METHODS = {
    'eq': operator.eq,
    'ne': operator.ne,
    'gt': operator.gt,
    'ge': operator.ge,
    'lt': operator.lt,
    'le': operator.le,
    'in': lambda x, y: x in y,
    'notin': lambda x, y: x not in y,
    'contains': lambda x, y: y in x,
    'istrue': lambda x: x is True,
    'isnull': lambda x: x is None,
    'notnull': lambda x: x is not None,
}


class Context:
    libraries = {}

    def __init__(self, config=None, variables=None):
        self.config = config
        variables = variables or {}
        self.variables = ChainMap(variables, os.environ)
        self.assert_methods = ASSERT_METHODS

    def get_variable(self, expr: str):
        if not isinstance(expr, str):
            return expr

        if DOLLAR_VARIABLE.match(expr):
            matched = PURE_DOLLAR_VARIABLE.match(expr)
            if matched:
                return get_field(self.variables, matched.group(1))
            return re.sub(DOLLAR_VARIABLE, self.repl_func, expr)
        return self.variables.get(expr, expr)

    def set_variable(self, key, value):
        if isinstance(value, str):
            value = self.get_variable(value)
        self.variables.update({key: value})

    def skip_check(self, skip_expr: Union[bool, str, list]) -> (bool, Optional[str]):
        if skip_expr is None:
            return None, None
        skip, skip_reason, *_ = skip_expr if isinstance(skip_expr, list) else (skip_expr, None)
        if isinstance(skip, str):
            skip = self.get_variable(skip)
            skip = eval(skip, {}, {}) is True
        if isinstance(skip, bool):
            return skip, skip_reason
        raise ValueError("Skip must be bool or str or list")

    def repl_func(self, matched):
        if matched:
            text = matched.group(1)
            return str(get_field(self.variables, text))

    def verify(self, item: dict):
        for method_name, method_args in item.items():
            method = self.get_assert_method(method_name)
            args, kwargs = get_args_kwargs(method_args, {})

            args = [self.get_variable(arg) for arg in args]  # actual, excepted
            kwargs = {key: self.get_variable(value) for key, value in kwargs.items()}
            assert method(*args, **kwargs), '%s failed! args: %s, kwargs: %s' % (method.__qualname__, args, kwargs)

    @classmethod
    def register_library(cls, library_class):
        cls.libraries[library_class.__name__] = library_class
        cls.__str__ = lambda self: self.__class__.__name__
        return library_class

    def get_assert_method(self, method_name: str):
        return self.assert_methods.get(method_name)

    def get_library(self, library_name: str):
        library_init_args = self.config.get(library_name, {}) if isinstance(self.config, dict) else {}
        args, kwargs = get_args_kwargs([], library_init_args)
        library_instance = self.libraries[library_name](*args, **kwargs)
        return library_instance


library = Context.register_library
