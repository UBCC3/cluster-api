import logging
import os
import subprocess
import shutil


# Configure logging
# TODO: Setup then logging to include root_dir
log_file_path = os.path.join("./", 'error_log.log')
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s:%(message)s')

def log_error(error_message):
    """Logs an error message using the logging module."""
    logging.error(error_message)
    
def get_slurm_id(db_job_id, root_dir) -> str:
    """
    Gets the ID given by slurm of the job
    Args: a string with the id given to the job by the db
    Returns: a string with the id given to the job by slurm
    """
    job_dir = os.path.join(root_dir+db_job_id)
    slurm_job_id = ""
    try:
        with open(job_dir + "/slurm_id.txt", "r") as file:
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

def is_job_in_queue(slurm_job_id) -> bool:
    """
    Checks if a job is still in the slurm queue
    Args:
    db_job_id: a str with the name of the job given by slurm
    Returns: true if job is in squeue, false otherwise
    """
    ssh_command = [
        "squeue", "--jobs", slurm_job_id
    ]
    squeue_result = subprocess.run(ssh_command, capture_output=True, text=True)

    if squeue_result.stdout:
        return True
    else:
        return False