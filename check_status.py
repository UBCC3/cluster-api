import os
import json
import subprocess
import zipfile

from main import root_dir
from util import get_slurm_id, log_error

def check_status(jobs_dict):
    for key in jobs_dict:
        jobs_dict[key] = check_job_queue(key)
    print(json.dumps(jobs_dict))

# check if the job is still in the queue or not
def check_job_queue(db_job_id):
    try:
        slurm_job_id = get_slurm_id(db_job_id)
        command = ["squeue", "--jobs", slurm_job_id]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # if the job is still pending or in progress
        if result.stdout: 
            return 0
        # if the job is completed or failed
        else:
            return check_job_status(db_job_id, slurm_job_id)
    except subprocess.CalledProcessError as e:
        log_error(f'Error: {e.stderr}')
        
# check the specifc job status when the job is not in the queue
def check_job_status(db_job_id, slurm_job_id):
    command = ["sacct", "--jobs", slurm_job_id, "--format=JobID,State,DerivedExitCode,Comment,Start,End"]
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
                    # TODO: process the result files into the one will be used in the platform
                    zip_output_files(db_job_id)
                    return {"state": state, "start_time": start_time, "end_time": end_time}
                else:
                    # Common status:
                    # CANCELLED: Job was cancelled by the user or a sysadmin
                    # FAILED: Job finished abnormally, with a non-zero exit code
                    # OUT_OF_MEMORY: Job was killed for using too much memory
                    # TIMEOUT: Job was killed for exceeding its time limit
                    comment = parts[comment_index] if comment_index is not None else "No additional info"
                    return {"state": state, "exitcode": derived_exit_code, "reason": comment}
    except subprocess.CalledProcessError as e:
        log_error(f'Error: {e.stderr}')
    
def zip_output_files(db_job_id):
    result_path = os.path.join(root_dir, db_job_id)
    output_zip_path = os.path.join(root_dir, "archive", f'{db_job_id}.zip')
    with zipfile.ZipFile(output_zip_path, 'w') as zip:
        for file in result_path:
            zip.write(file)
    