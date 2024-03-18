from python_tdl import schema





class StepResult(schema.TestCaseResult):
    def __init__(self, step):
        self.step_id = step.id
        self.step_name = step.name
        self.start_time = None
        self.end_time = None
        self.status = None
        self.is_success = None


class TestCaseRecord(schema.TestCaseResult):
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.status = None
        self.is_success = None
        self.details = []


class TestCaseResult(schema.TestCaseResult):
    def __init__(self, testcase):
        self.testcase_id = testcase.id
        self.testcase_name = testcase.name
        self.start_time = None
        self.end_time = None
        self.status = None
        self.is_success = None
        self.records = []


class TestResult(schema.TestResult):
    def __init__(self, testsuite, title: str, description: str = None):
        self.title = title
        self.description = description

        self.testsuite_id = testsuite.id
        self.testsuite_name = testsuite.name
        self.start_time = None
        self.end_time = None
        self.status = None
        self.is_success = None
        self.details = []
