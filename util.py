import logging
import os

import shutil

from main import root_dir

# Configure logging
log_file_path = os.path.join(root_dir, 'error_log.log')
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s:%(message)s')

def log_error(error_message):
    """Logs an error message using the logging module."""
    logging.error(error_message)
    
def get_slurm_id(db_job_id) -> str:
    """
    Gets the ID given by slurm of the job
    Args: a string with the id given to the job by the db
    Returns: a string with the id given to the job by slurm
    """
    current_path = os.path.join("./"+db_job_id)
    slurm_job_id = ""
    try:
        with open(current_path + "/slurm_id.txt", "r") as file:
            slurm_job_id = file.readline()
        return slurm_job_id
    except FileNotFoundError as error:
        log_error(error)
    
def clean_up(current_path):
    """
    Deletes a job's directory
    Args:
    script_path: a str with the name of the job which will be used as directory name
    Returns: true if success, false otherwise
    """
    try:
        shutil.rmtree(current_path)
    except:
        return False
    else:
        return True
