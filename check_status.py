import subprocess

# check if the job is still in the queue or not
def check_job_queue(db_job_id):
    slurm_job_id =  fetch_slurm_job_id(db_job_id)
    command = f'squeue --jobs {slurm_job_id}'
    ssh_command = ["ssh cluster", command]
    
    try:
        result = subprocess.run(ssh_command, capture_output=True, text=True, check=True)
        # if the job is still pending or in progress
        if result.stdout: 
            # TODO: can be updated with a more helpful return message
            print("still running") 
        # if the job is completed or failed
        else:
            return check_job_status(db_job_id, slurm_job_id)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")

# fetch the job id in the slurm system using the the value of job id in the database
def fetch_slurm_job_id(db_job_id):
    # TODO: update "slurm_id" with the actual file name that stores the job id in slurm system
    file_path = f'scratch/ubchemica/{db_job_id}/slurm_id.txt'
    command = f'cat {file_path}'
    ssh_command = ["ssh cluster", command]
    
    try:
        result = subprocess.run(ssh_command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
        
# check the specifc job status when the job is not in the queue
def check_job_status(db_job_id, slurm_job_id):
    command = f'sacct --jobs {slurm_job_id} --format=JobID,State,DerivedExitCode,Comment'
    ssh_command = ["ssh cluster", command]
    
    try:
        result = subprocess.run(ssh_command, capture_output=True, text=True, check=True)
        # Sample result.stdout
        # JobID           State      DerivedExitCode    ....
        # ------------    ---------- --------
        # 12345           COMPLETED  0:0
        # 12345.batch     COMPLETED  0:0
        # 12345.0         FAILED     49:0
        lines = result.stdout.splitlines()
        header = lines[0].split()
        job_index = header.index("JobID")
        state_index = header.index("State")
        derived_exit_code_index = header.index("DerivedExitCode")
        comment_index = header.index("Comment") if "Comment" in header else None
        
        for line in lines[2:]:
            parts = line.split()
            if parts[job_index] == str(slurm_job_id):
                state = parts[state_index]
                derived_exit_code = parts[derived_exit_code_index]
                if state == "COMPLETED" and derived_exit_code == "0:0":
                    print(f'Job {db_job_id} is completed')
                else:
                    # Common status:
                    # CANCELLED: Job was cancelled by the user or a sysadmin
                    # FAILED: Job finished abnormally, with a non-zero exit code
                    # OUT_OF_MEMORY: Job was killed for using too much memory
                    # TIMEOUT: Job was killed for exceeding its time limit
                    comment = parts[comment_index] if comment_index is not None else "No additional info"
                    print(f"Job {db_job_id} failed with exit code {derived_exit_code}. Reason: {comment}")    
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
        