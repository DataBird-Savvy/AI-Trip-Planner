
import sys


class AITripPlannerException(Exception):

    def __init__(self, error_message, error_detail=None):

        self.error_message = self.get_detailed_error_message(
            error_message,
            error_detail
        )

        super().__init__(self.error_message)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail=None):

        if error_detail is None:
            return str(error_message)

        # error_detail is already a tuple from sys.exc_info()
        _, _, exec_tb = error_detail

        if exec_tb is None:
            return str(error_message)

        file_name = exec_tb.tb_frame.f_code.co_filename
        line_number = exec_tb.tb_lineno

        return (
            f"Error occurred in script: [{file_name}] "
            f"at line number: [{line_number}] "
            f"error message: [{error_message}]"
        )
