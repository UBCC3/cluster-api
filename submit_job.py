import sys
import json
import subprocess

# TODO: Add S3 Upload
# TODO: Add clean up scripts
def write_sbatch_script(job_name, command):
    with open("submit_job.sh", "w") as file:
        file.write(f'''#!/bin/bash
        #SBATCH --job-name={job_name}
        #SBATCH --output={job_name}.out
        #SBATCH --error={job_name}.err
        mkdir {job_name}
        cd {job_name}
        {command}

        cd ..
        rm -r {job_name}
        ''')
def submit_sbatch_script(script_path):
    result = subprocess.run(['sbatch', script_path], capture_output=True, text=True)
    print(result)
# NOTE: Input JSON cannot have any spaces in it
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Too many arguments: ", len(sys.argv), "\nUsage: python3 submit_job.py '{json details}'")

    job_input_data = json.loads(sys.argv[1])
    job_sql_id = job_input_data["id"]
    job_basis_set = job_input_data["basisSet"]
    job_theory = job_input_data["theory"]
    job_wave_theory = job_input_data["waveTheory"]
    job_calculation_type = job_input_data["calculation"]
    job_solvent_effects = job_input_data["solventEffects"]
    script_path = "./" + job_sql_id + "submit_job.sh"
    write_sbatch_script("testing", 'echo "bruh"')
    submit_sbatch_script(script_path)


