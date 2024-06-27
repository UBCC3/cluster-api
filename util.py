import logging
import os

from main import root_dir

log_file_path = os.path.join(root_dir, 'error_log.log')
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s:%(message)s')

def log_error(error_message):
    """Logs an error message using the logging module."""
    logging.error(error_message)
