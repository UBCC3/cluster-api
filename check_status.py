import subprocess

from util import get_slurm_id, log_error

def check_status(parameters):
    """
    Check the status of jobs whose status is pending or in progress in the database 
    Args:
        parameters: a dictionary that contains:
            - jobs_dict: a dictionary where the key is the db_job_id, and the value is the db_job_status
            - root_dir (str): the root directory path
    Returns:
        a dictionary where the key is the db_job_id, and the value is 0 (nothing change for the job) or a dictionary with updated job information
    """
    jobs_dict = parameters["jobs_dict"]
    root_dir = parameters["root_dir"]
    try:   
        for key, value in jobs_dict.items():
            jobs_dict[key] = check_job_queue(key, value, root_dir)
        return jobs_dict
    except Exception as e:
        log_error(e, root_dir)  
        # TODO: return something to the backend

def check_job_queue(db_job_id, db_job_status, root_dir):
    """
    Check if the job is still in the queue or not
    Args:
        db_job_id (str): job ID in the database
        db_job_status (str): current status in the database ('SUBMITTED' or 'RUNNING')
        root_dir (str): the root directory path
    Returns:
        0 (nothing change for the job) or a dictionary with additional job information
    """
    slurm_job_id = get_slurm_id(db_job_id, root_dir)
    try:
        command = ["squeue", "-j", slurm_job_id, "--Format=State,StartTime"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
    except:
        return check_job_status(slurm_job_id)
    else:
        lines = result.stdout.splitlines()
        job_info = lines[1].split()
        if job_info[0] == "RUNNING" and db_job_status == "SUBMITTED":
            return {"status": "RUNNING", "started": job_info[1]}
        return 0

def check_job_status(slurm_job_id):
    """
    Check the job information when the job is not in the queue (CANCELLED, FAILED, OUT_OF_MEMORY, TIMEOUT, ...)
    Args:
        slurm_job_id (str): job ID in the Slurm system
    Returns: 
        a dictionary with additional job information
    """
    command = ["sacct", "-j", slurm_job_id, "--format=JobID,State,Start,End,DerivedExitCode,Comment"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        """
        Sample result.stdout
        JobID           State      DerivedExitCode    ....
        ------------    ---------- --------
        12345           COMPLETED  0:0
        12345.batch     COMPLETED  0:0
        12345.0         FAILED     49:0
        """
        lines = result.stdout.splitlines()
        header = lines[0].split()
        job_index = header.index("JobID")
        state_index = header.index("State")
        derived_exit_code_index = header.index("DerivedExitCode")
        comment_index = header.index("Comment")
        start_index = header.index("Start")
        end_index = header.index("End")
        for line in lines[2:]:
            parts = line.split()
            if parts[job_index] == str(slurm_job_id):
                state = parts[state_index]
                derived_exit_code = parts[derived_exit_code_index]
                start_time = parts[start_index]
                end_time = parts[end_index]
                if state == "COMPLETED" and derived_exit_code == "0:0":
                    return {"status": "COMPLETED", "started": start_time, "finished": end_time}
                elif state == "CANCELLED" or state == "CANCELLED+":
                    return {"status": "CANCELLED", "started": start_time, "finished": end_time}
                else:
                    comment = parts[comment_index] if comment_index < len(parts) else "No additional info"
                    return {"status": "FAILED", "started": start_time, "finished": end_time, "error_message": comment}
    except subprocess.CalledProcessError as e:
        raise Exception(f'Error running sacct: {e.stderr}')
    
