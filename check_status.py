import subprocess

from util import get_slurm_id, log_error

def check_status(parameters):
    """
    Check the status of jobs whose status is pending or in progress in the database 
    Input: 
        - parameters: a dictionary that contains:
            - jobs_dict: a dictionary where the key is the db_job_id, and the value is the db_job_status
            - root_dir: the root directory path
    Output:
        -  a dictionary where the key is the db_job_id, and the value is 0 (nothing change for the job) or a dictionary with updated job information
    """
    jobs_dict = parameters[jobs_dict]
    root_dir = parameters[root_dir]
    try:   
        for key, value in jobs_dict.items():
            jobs_dict[key] = check_job_queue(key, value)
        return jobs_dict
    except Exception as e:
        log_error(e, root_dir)  
        # TODO: return something to the backend

def check_job_queue(db_job_id, db_job_status):
    """
    Check if the job is still in the queue or not
    Input:
        - db_job_id: job ID in the database
        - db_job_status: current status in the database ('submitted' or 'running')
    output: 
        - 0 (nothing change for the job) or a dictionary with additional job information
    """
    try:
        slurm_job_id = get_slurm_id(db_job_id)
        command = ["squeue", "--jobs", slurm_job_id, "--format=State,StartTime"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stdout:  # if the job is still pending or running
            lines = result.stdout.splitlines()
            job_info = lines[1].split()
            if job_info[0] == "RUNNING" and db_job_status == "submitted":
                return {"status": "running", "started": job_info[1]}
            return 0
        else: # if the job is completed or failed
            check_job_status(slurm_job_id)    
    except subprocess.CalledProcessError as e:
        raise Exception(f'Error running squeue for job ID {db_job_id}: {e.stderr}')       
        
def check_job_status(slurm_job_id):
    """
    Check the job information when the job is not in the queue (CANCELLED, FAILED, OUT_OF_MEMORY, TIMEOUT, ...)
    Input:
        - slurm_job_id: job ID in the Slurm system
    Output: 
        - a dictionary with additional job information
    """
    command = ["sacct", "--jobs", slurm_job_id, "--format=JobID,State,DerivedExitCode,Comment,Start,End"]
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
        comment_index = header.index("Comment") if "Comment" in header else None
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
                    return {"status": "completed", "started": start_time, "finished": end_time}
                else:
                    comment = parts[comment_index] if comment_index is not None else "No additional info"
                    return {"status": "failed", "started": start_time, "finished": end_time, "error_message": comment}
    except subprocess.CalledProcessError as e:
        raise Exception(f'Error running sacct: {e.stderr}')
    