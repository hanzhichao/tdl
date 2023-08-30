class Context:
    libraries = {}

    def __init__(self, config=None, variables=None):
        self.config = config
        self.variables = variables

    @classmethod
    def register_library(cls, library_class):
        cls.libraries[library_class.__name__] = library_class
        return library_class

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


library = Context.register_library
