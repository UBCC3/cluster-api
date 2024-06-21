import subprocess
import os
import shutil

def clean_job(script_path: str) -> bool:
    """
    Deletes a job's directory

    Args:
    script_path: a str with the name of the job which will be used as directory name

    Returns: true if success, false otherwise
    """
    try:
        shutil.rmtree(script_path)
    except:
        return False
    else:
        return True