import os
import sys
import pandas as pd
import numpy as np


import os
import pickle
from src.exception import CustomException
from src.logger import logging


def save_object(obj, file_path):
    """
    Saves a Python object to the specified file path using pickle.

    Args:
        obj: The Python object to save.
        file_path (str): The path where the object will be saved.

    Raises:
        Exception: If the object cannot be saved.
    """
    try:
        # Ensure the directory exists
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # Save the object
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        raise Exception(f"Error saving object: {e}")
