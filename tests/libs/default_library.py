from tdl.context import library


@library
class Default:
    def log(self, *args, **kwargs):
        print(*args, **kwargs)

    def eq(self, actual, excepted):
        return excepted == actual
