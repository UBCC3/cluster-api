import os
import subprocess

def get_slurm_id(db_job_id):
    current_path = os.path.join("./"+db_job_id)
    slurm_job_id = ""
    try:
        with open(current_path + "/slurm_id.txt", "r") as file:
            slurm_job_id = file.readLine()
    except FileNotFoundError as error:
        raise error
    else:
        return slurm_job_id

def clean_up(current_path):
    subprocess.run(["sbatch", current_path + "/clean_up.sh"],capture_output=True, text=True)