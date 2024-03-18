import pytest

import tests.libs
from tdl import Env

libs = tests.libs


@pytest.fixture
def env():
    env = Env('test', config={'Http': {'base_url': 'http://postman-echo.com'}})
    return env


@pytest.fixture
def context(env):
    return env.context
