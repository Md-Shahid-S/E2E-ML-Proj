import os
from datetime import datetime
import logging

# Define log file and path
log_file = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_logfile.log"
logs_path = os.path.join(os.getcwd(), "logs")  # Absolute path to logs folder
log_file_path = os.path.join(logs_path, log_file)

# Make sure the logs folder exists
os.makedirs(logs_path, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
)

if __name__ == "__main__":
    # Example usage
    logging.info("This is an info message.")
    logging.error("This is an error message.")
    logging.warning("This is a warning message.")
    logging.debug("This is a debug message.")
    logging.critical("This is a critical message.")