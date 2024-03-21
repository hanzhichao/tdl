from . import schema
from .context import Context


class Env(schema.Env):
    def __init__(self, name: str = None, config: dict = None, variables: dict = None):
        self.name = name
        self.config = config or {}
        self.variables = variables or {}

    @property
    def context(self) -> Context:
        return Context(config=self.config, variables=self.variables)

    @property
    def info(self):
        return dict(name=self.name, config=self.config, variables=self.variables)
