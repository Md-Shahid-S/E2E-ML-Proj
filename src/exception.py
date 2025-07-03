# src/exception.py
import sys
from src.logger import logging

def error_message_details(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return f"Error occurred in script: [{file_name}] at line number: [{line_number}] error message: [{str(error)}]"

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(str(error_message))
        self.error_message = error_message_details(error_message, error_detail)
        logging.error(self.error_message)  # <-- Log happens here

    def __str__(self):
        return self.error_message

# test block
if __name__ == "__main__":
    try:
        a = 1 / 0
    except Exception as e:
        raise CustomException(e, sys)
