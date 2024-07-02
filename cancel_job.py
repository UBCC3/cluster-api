import subprocess
import os
from .util import get_slurm_id, clean_up
def cancel_job(job_input_data) -> bool:
    """
    Cancels a job queued/currently running

    Args: a JSON with all the job input data

    Returns: True if job was successfully cancelled, False otherwise
    """
    slurm_job_id = get_slurm_id(job_input_data["id"])
    job_dir = os.path.join(job_input_data["root_dir"]+job_input_data["id"])
    cancel_command = [
        "scancel", slurm_job_id
    ]
    subprocess.run(cancel_command, capture_output=True, text=True)
    if clean_up(job_dir):
        print("{'status':'SUCCESS'}")
    else:
        raise Exception("FAILED")