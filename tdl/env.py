from . import schema
from .context import Context


class Env(schema.Env):
    def __init__(self, name: str, config: dict = None, variables: dict = None):
        self.name = name
        self.config = config
        self.variables = variables

        self.context = Context(config=config, variables=variables)

    @property
    def info(self):
        return dict(name=self.name, config=self.config, variables=self.variables)
