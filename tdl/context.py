from functools import reduce
import importlib
import os
from collections import ChainMap
import re

DOLLAR_VARIABLE = re.compile('\${?([\w.]+)}?')
PURE_DOLLAR_VARIABLE = re.compile('^\${?([\w.]+)}?$')


def do_dot(item, key: str):
    """单个content.url取值"""  # result.url
    if hasattr(item, key):
        return getattr(item, key)

    if key.isdigit():  # result.1  # []
        key = int(key)
    try:
        return item[key]  # result[1] / result[key]

    except Exception as ex:
        return key  # result.url


class Context:
    libraries = {}

    def __init__(self, config=None, variables=None):
        self.config = config or {}
        self.variables = variables or {}

    def get_method(self, method_expr: str):
        if '.' in method_expr:
            library_name, method_name = method_expr.split('.', 1)
        else:
            library_name, method_name = 'default', method_expr

        if self.config is None:
            init_args = {}
        else:
            init_args = self.config.get(library_name, {})

        args = init_args if isinstance(init_args, list) else []
        kwargs = init_args if isinstance(init_args, dict) else {}

        method_library = self.libraries[library_name](*args, **kwargs)
        method = getattr(method_library, method_name)
        return method

    def repl_func(self, matched):
        if matched:
            text = matched.group(1)
            return str(self._get_field(text))

    def _get_field(self, expr: str):
        """解析形如content.result.0.id的取值"""
        if '.' in expr:
            value = expr.split('.')
            field = self.variables.get(value[0])
            return reduce(lambda x, y: do_dot(x, y), value[1:], field)
        else:
            return self.variables.get(expr)

    def get(self, expr: str):
        if not isinstance(expr, str):
            return expr
        if DOLLAR_VARIABLE.match(expr):
            matched = PURE_DOLLAR_VARIABLE.match(expr)
            if matched:
                return self._get_field(matched.group(1))
            return re.sub(DOLLAR_VARIABLE, self.repl_func, expr)
        return self.variables.get(expr, expr)

    def set(self, key, value):
        if not isinstance(key, str):
            key = str(key)
        if isinstance(value, str):
            value = self.get(value)
        self.variables.update({key: value})


    @classmethod
    def register_library(cls, library_class):
        cls.libraries[library_class.__name__] = library_class


library = Context.register_library

# def library(library_class):
#     Context.libraries[library_class.__name__] = library_class
