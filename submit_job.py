import json
import subprocess
import os
from .util import clean_up

# TODO: Add S3 Upload
# TODO: Modify code for Psi4 and QCEngine
def write_sbatch_script(job_name):
    """
    Sets up a directory with the job_name as its name.
    Creates an sbatch script to be run.

    Args:
    - A string that has the name of the job which will be used as dir name.
    
    Returns: None
    """
    try:
        os.mkdir(job_name)
    except OSError as error:
        print(error)
    job_dir = os.path.join(root_dir+job_name)
    with open(job_dir + "/submit_job.sh", "w") as file:
        file.write(f'''#!/bin/bash
        #SBATCH --job-name={job_name}
        #SBATCH --output={job_name}.out
        #SBATCH --error={job_name}.err
        echo "Hello"



        ''')


def submit_sbatch_script(script_path):
    """
    Submits the job to SLURM via sbatch

    Args: The path to the submit_job bash file

    Returns: None
    """
    result = subprocess.run(["sbatch", script_path  + "/submit_job.sh"], capture_output=True, text=True)
    try:
        slurm_job_id = (result.stdout.split()[-1])
        current_path = os.path.join(root_dir, script_path)
        with open(current_path + "/slurm_id.txt", "w") as file:
            file.write(slurm_job_id)
    except:
        clean_up_result = clean_up(script_path)
        return "{'status':'FAILURE'}"
        
    else:
        return "{'status':'SUCCESS'}"

def submit_job(job_input_data: dict) -> None:
    db_job_id = job_input_data["id"]
    job_basis_set = job_input_data["basisSet"]
    job_theory = job_input_data["theory"]
    job_wave_theory = job_input_data["waveTheory"]
    job_calculation_type = job_input_data["calculation"]
    job_solvent_effects = job_input_data["solventEffects"]
    script_path = os.path.join(root_dir, db_job_id)
    write_sbatch_script(db_job_id)
    submit_sbatch_script(script_path)


