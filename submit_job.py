import json
import subprocess
import os
import sys
from util import clean_up, log_error

nstasks = 1
max_walltime = "00:05"
psi4_env_dir = os.environ.get("PSI4_ENV_DIR")
qcEngine_script_loc = os.environ.get("QCENGINE_SCRIPT_LOC")

# TODO: Add S3 Upload
# TODO: Modify code for Psi4 and QCEngine
def write_sbatch_script(job_dir: str, script_path: str, job_input_data: dict):
    """
    Creates an sbatch script to be run.
    
    Args:
    job_dir - path to directory in which job will run
    script_path - path to sbatch script
    job_input_data - dictionary containing all job input information

    Returns: None
    """
    job_name = job_input_data["id"]
    job_basis_set = job_input_data["basisSet"]
    job_theory = job_input_data["theory"]
    job_wave_theory = job_input_data["waveTheory"]
    job_calculation_type = job_input_data["calculation"]
    job_solvent_effects = job_input_data["solventEffects"]
    job_structure_dir = os.path.join(job_dir, "job_structure.xyz")
    with open(job_structure_dir, "w") as file:
        file.write(job_input_data["job_structure"])

    with open(script_path, "w") as file:
        file.write(f'''#!/bin/bash
    #SBATCH --job-name={job_name}
    #SBATCH --output=f'{job_dir}/{job_name}.out'
    #SBATCH --error=f'{job_dir}/{job_name}.err'
    #SBATCH --nstasks = {nstasks}
    #SBATCH --mem-per-cpu=1024M
    #SBATCH --time={max_walltime}


    cd {job_dir}
    module load StdEnv/2023
    module load gcc/12.3
    module load openmpi/4.1.5
    module load psi4/1.9

    source {psi4_env_dir}
    basisSet="{job_basis_set}"
    method="{job_theory}"
    calculationType="{job_calculation_type}"
    structure = "{job_structure_dir}"
    python3 {qcEngine_script_loc} "$calculationType" "$method" "$basisSet" "$structure"

        ''')

def submit_sbatch_script(job_dir: str, script_path: str):
    """
    Submits the job to SLURM via sbatch

    Args: job_dir - directory in which job runs
          script_path - path to the submit_job bash file

    Returns: None
    """

    try:
        result = subprocess.run(["sbatch", script_path], capture_output=True, text=True)
        slurm_job_id = (result.stdout.split()[-1])
        with open(job_dir + "/slurm_id.txt", "w") as file:
            file.write(slurm_job_id)
    except:
        clean_up_result = clean_up(job_dir)
        return {'status':'FAILURE'}
        
    else:
        return {'status':'SUCCESS'}

def submit_job(job_input_data: dict) -> None:
    root_dir = job_input_data["root_dir"]
    db_job_id = job_input_data["id"]
    job_dir = os.path.join(root_dir, db_job_id)
    script_path = os.path.join(job_dir, "submit_job.sh")

# create directory in which job will run
# note: if root_dir is not writable, then log_error will also fail here.

    try:
        os.mkdir(job_dir)
    except OSError as error:
        log_error(error, root_dir) # log stderr to keep standard output clean

# create sbatch script and then submit it

    try:
        write_sbatch_script(job_dir, script_path, job_input_data)
    except:
        clean_up_result = clean_up(job_dir)
        return {'status':'FAILURE'}
    else:
        return submit_sbatch_script(job_dir, script_path)
