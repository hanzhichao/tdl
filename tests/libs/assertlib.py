from tdl.context import library


@library
class Assert:
    NO_STORE_RESULT = True

    @staticmethod
    def eq(actual, expected):
        assert actual == expected, f'断言失败: 实际值 {actual} 不等于 期望值 {expected}'

    @staticmethod
    def str_eq(self, actual, expected):
        assert str(actual) == str(expected), f'断言失败: 实际值 {actual} 不等于 期望值 {expected}'

    @staticmethod
    def contains_by(self, actual, expected):
        assert actual in expected, f'断言失败: 期望值 {expected} 不包含 实际值 {actual}'

    @staticmethod
    def contains(self, actual, expected):
        print('actual', actual)
        print('expected', expected)
        assert expected in actual, f'断言失败: 实际值 {actual} 不包含 期望值 {expected}'

    @staticmethod
    def istrue(self, actual):
        assert actual is True, f'断言失败: 实际值 {actual} 不为True'

    @staticmethod
    def nottrue(self, actual):
        assert actual is not True, f'断言失败: 实际值 {actual} 为True'

    @staticmethod
    def isnull(self, actual):
        assert actual is None, f'断言失败: 实际值 {actual} 不为None'

    @staticmethod
    def notnull(self, actual):
        assert actual is not None, f'断言失败: 实际值 {actual} 为None'
