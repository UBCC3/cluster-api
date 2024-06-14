import json
import subprocess
import sys

# check if the job is still in the queue or not
def check_job_queue(db_job_id):
    try:
        slurm_job_id =  fetch_slurm_job_id(db_job_id)
        command = ["squeue", "--jobs", slurm_job_id]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # if the job is still pending or in progress
        if result.stdout: 
            return 0
        # if the job is completed or failed
        else:
            return check_job_status(db_job_id, slurm_job_id)
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    except Exception as e:
        return str(e)

# fetch the job id in the slurm system using the the value of job id in the database
def fetch_slurm_job_id(db_job_id):
    # TODO: update "slurm_id" with the actual file name that stores the job id in slurm system
    file_path = f'scratch/ubchemica/{db_job_id}/slurm_id.txt'
    command = ["cat", file_path]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error: {e.stderr}")
        
# check the specifc job status when the job is not in the queue
def check_job_status(db_job_id, slurm_job_id):
    command = ["sacct", "--jobs", slurm_job_id, "--format=JobID,State,DerivedExitCode,Comment"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
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
                    # TODO: process the result files into the one will be used in the platform and a zipped one
                    return 1
                else:
                    # Common status:
                    # CANCELLED: Job was cancelled by the user or a sysadmin
                    # FAILED: Job finished abnormally, with a non-zero exit code
                    # OUT_OF_MEMORY: Job was killed for using too much memory
                    # TIMEOUT: Job was killed for exceeding its time limit
                    comment = parts[comment_index] if comment_index is not None else "No additional info"
                    return json.dumps({"exitcode": derived_exit_code, "reason": comment})
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error: {e.stderr}")

if __name__ == "__main__":
    """
    Sample input:
    {
        "jobid1": 0,
        "jobid2": 0,
        "jobid3": 0
    }
    for each value:
    - 0 indicate the job is still pending or inprogress
    - 1 indicate the job is completed
    - ...
    """
    input_data = json.load(sys.stdin)
    for key in input_data:
        input_data[key] = check_job_queue(input_data[key])
    print(json.dumps(input_data))
    