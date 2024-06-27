import subprocess
import os
from .util import get_slurm_id, clean_up
from main import root_dir
def cancel_job(job_input_data) -> bool:
    """
    Cancels a job queued/currently running

    Args: a JSON with all the job input data

    Returns: True if job was successfully cancelled, False otherwise
    """
    slurm_job_id = get_slurm_id(job_input_data["id"])
    current_path = os.path.join(root_dir+job_input_data["id"])
    cancel_command = [
        "scancel", slurm_job_id
    ]
    subprocess.run(cancel_command, capture_output=True, text=True)
    if clean_up(current_path):
        print("{'status':'SUCCESS'}")
    else:
        raise Exception("FAILED")