import sys
import logging

def error_message_details(error, error_detail: sys):
    """
    Generates a detailed error message with filename, line number, and error description.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return f"Error occurred in script: [{file_name}] at line number: [{line_number}] error message: [{str(error)}]"

class CustomException(Exception):
    """
    Custom exception class for better error tracking and debugging.
    """
    def __init__(self, error_message, error_detail: sys):
        super().__init__(str(error_message))
        self.error_message = error_message_details(error_message, error_detail)

    def __str__(self):
        return self.error_message

# Optional test block
if __name__ == "__main__":
    try:
        a = 1 / 0  # Intentional error
    except Exception as e:
        custom_error = CustomException(e, sys)
        print(custom_error)
    finally:
        print("This is the end of the script.")
