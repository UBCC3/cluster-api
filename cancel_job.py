import subprocess
import os
from .util import get_slurm_id, clean_up, is_job_in_queue
def cancel_job(job_input_data) -> bool:
    """
    Cancels a job queued/currently running

    Args: a JSON with all the job input data

    Returns: True if job was successfully cancelled, False otherwise
    """
    slurm_job_id = get_slurm_id(job_input_data["id"], job_input_data["root_dir"])
    if is_job_in_queue(slurm_job_id):
        job_dir = os.path.join(job_input_data["root_dir"]+job_input_data["id"])
        cancel_command = [
            "scancel", slurm_job_id
        ]
        cancel_result = subprocess.run(cancel_command, capture_output=True, text=True)
        if not cancel_result.stderr:
            return {'status':'SUCCESS'}
        else:
            return {'status':'FAILURE'}
    else:
        return {'status':'FAILURE'}