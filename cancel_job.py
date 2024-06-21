import subprocess
import os
def find_job_id(job_name):
    current_path = os.path.join("./"+job_name)
    slurm_job_id = ""
    try:
        with open(current_path + "/slurm_id.txt", "r") as file:
            slurm_job_id = file.readLine()
            cancel_command = [
                "scancel", slurm_job_id
            ]
        subprocess.run(cancel_command, capture_output=True, text=True)
        subprocess.run(["sbatch", current_path + "/clean_up.sh"],capture_output=True, text=True)
    except FileNotFoundError as error:
        raise error
    return True
def cancel_job(db_job_id: str) -> bool:
    find_job_id(db_job_id)