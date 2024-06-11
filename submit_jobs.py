import sys
import json
import subprocess

if len(sys.argv) != 2:
    raise Exception("Usage: python3 submit_jobs.py '{json details}'")

job_input_data = json.loads(sys.argv[1])
job_theory = job_input_data["theory"]
job_basis_set = job_input_data["basisSet"]
job_wave_theory = job_input_data["waveTheory"]
job_calculation_type = job_input_data["calculation"]
job_solvent_effects = job_input_data["solventEffects"]
job_sql_id = job_input_data["id"]

# TODO: Add S3 Upload
# TODO: Add clean up scripts
def write_sbatch_script(job_name, command):
    with open("submit_job.sh", "w") as file:
    f.write(f'''#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={job_name}.out
#SBATCH --error={job_name}.err
mkdir {job_name}
cd {job_name}
{command}

cd ..
rm -r {job_name}
''')
script_path = "./" + job_sql_id + "submit_job.sh"
def run_sbatch_script(script_path):
    subprocess.run(['sbatch', script_path])

write_sbatch_script(script_path, job_sql_id)
submit_sbatch_script(script_path)
