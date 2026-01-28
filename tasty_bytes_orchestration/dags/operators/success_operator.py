import logging
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SuccessLogOperator(BaseOperator):
    """
    A simple custom operator that logs a success message.
    """

    @apply_defaults
    def __init__(self, custom_message: str = "Job completed successfully!", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_message = custom_message

    def execute(self, context):
        # This is where the custom logic happens
        logging.info("------------------------------------------------")
        logging.info(f"CUSTOM OPERATOR SIGNAL: {self.custom_message}")
        logging.info("------------------------------------------------")
        return "Success Signal Sent"