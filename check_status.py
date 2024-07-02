import subprocess

from util import get_slurm_id, log_error

def check_status(jobs_dict):
    """
    check the status of jobs whose status is pending or in progress in the database 
    input: dictionary where key is the db_job_id, and value is the db_job_status (PENDING or RUNNING)
    output: dictionary where key is the db_job_id, and value is a dictionary with additional job information
    """
    for key, value in jobs_dict.item():
        jobs_dict[key] = check_job_queue(key, value)
    return jobs_dict

def check_job_queue(db_job_id, db_job_status):
    """
    check if the job is still in the queue or not
    input: db_job_id and db_job_status
    output: a dictionary with additional job information
    """
    try:
        slurm_job_id = get_slurm_id(db_job_id)
        command = ["squeue", "--jobs", slurm_job_id, "--format=State,StartTime"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stdout:  # if the job is still pending or running
            if db_job_status == "RUNNING":
                return db_job_status
            else: # db_job_status == "pending":
                lines = result.stdout.splitlines()
                job_info = lines[1].split()
                if job_info[0] != db_job_status:
                    return {"status": job_info[0], "started": job_info[1]}
                else:
                    return db_job_status
        else: # if the job is completed or failed
            check_job_status(slurm_job_id)    
    except subprocess.CalledProcessError as e:
        log_error(f'Error: {e.stderr}')
        
def check_job_status(slurm_job_id):
    """
    check the specifc job information when the job is not in the queue (CANCELLED, FAILED, OUT_OF_MEMORY, TIMEOUT, ...)
    input: slurm_job_id
    output: a dictionary with additional job information
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
                if state == "COMPLETED" and derived_exit_code == "0:0":
                    start_time = parts[start_index]
                    end_time = parts[end_index]
                    return {"status": state, "started": start_time, "finished": end_time}
                else:
                    comment = parts[comment_index] if comment_index is not None else "No additional info"
                    return {"status": state, "started": start_time, "finished": end_time, "error_message": comment}
    except subprocess.CalledProcessError as e:
        log_error(f'Error: {e.stderr}')
    