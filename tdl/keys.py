import os


class StepKeys:
    name = os.getenv('TDL_KEY_STEP_NAME') or 'name'
    method = os.getenv('TDL_KEY_STEP_NAME') or 'method'
