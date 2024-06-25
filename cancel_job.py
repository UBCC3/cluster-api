import subprocess
import os
from .util import get_slurm_id, clean_up
def cancel_job(job_input_data) -> bool:
    slurm_job_id = get_slurm_id(job_input_data["id"])
    current_path = os.path.join("./"+job_name)
    cancel_command = [
        "scancel", slurm_job_id
    ]
    subprocess.run(cancel_command, capture_output=True, text=True)
    clean_up(current_path)
    