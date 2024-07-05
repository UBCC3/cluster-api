import datetime
import os

import shutil

def log_error(error_message, root_dir):
    """
    Logs an error message to the text file with the current timestamp
    Args:
        error_message (str): The error message to log.
        root_dir (str): the root directory path
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_file_dir = os.path.join(root_dir, 'error_log.txt')
    with open(error_file_dir, "a") as file:
        file.write(f"{current_time}: {error_message}\n")
    
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
