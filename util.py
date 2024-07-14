import datetime
import os
import subprocess
import shutil
from openbabel import openbabel

def convert_file_to_xyz(input_string, job_directory):
    obc = openbabel.OBConversion()
    obc.SetOutFormat("xyz")

    structure = openbabel.OBMol()
    obc.ReadString(input_string)

    obc.WriteFile(structure, job_directory.replace("pdb","xyz"))

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
    
def get_slurm_id(db_job_id, root_dir) -> str:
    """
    Gets the ID given by slurm of the job
    Args: a string with the id given to the job by the db
    Returns: a string with the id given to the job by slurm
    """
    job_dir = os.path.join(root_dir, db_job_id)
    slurm_job_id = ""
    try:
        with open(job_dir + "/slurm_id.txt", "r") as file:
            slurm_job_id = file.readline()
        return slurm_job_id
    except FileNotFoundError as error:
        log_error(error, root_dir)
    
def clean_up(job_dir):
    """
    Deletes a job's directory
    Args:
    script_path: a str with the name of the job which will be used as directory name
    Returns: true if success, false otherwise
    """
    try:
        shutil.rmtree(job_dir)
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
