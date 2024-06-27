import logging

logging.basicConfig(filename='error_log.log', level=logging.ERROR, format='%(asctime)s:%(message)s')

def log_error(error_message):
    """Logs an error message using the logging module."""
    logging.error(error_message)
