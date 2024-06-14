import json
import subprocess
import os
# TODO: Add S3 Upload
# TODO: Add clean up scripts
def write_sbatch_script(job_name, command):
    try:  
        os.mkdir(job_name)  
    except OSError as error:  
        print(error) 
    cur_path = os.path.join("./"+job_name)
    with open(cur_path + "/submit_job.sh", "w") as file:
        file.write(f'''#!/bin/bash
        #SBATCH --job-name={job_name}
        #SBATCH --output={job_name}.out
        #SBATCH --error={job_name}.err
        {command}

        ''')
    with open(cur_path + "/clean_up.sh", "w") as file:
        file.write(f'''#!/bin/bash
        rm -r {job_name}
                   ''')
def submit_sbatch_script(script_path):
    result = subprocess.run(["sbatch", script_path  + "/submit_job.sh"], capture_output=True, text=True)
    print(result)
    clean_up_result = subprocess.run(["sbatch", script_path + "/clean_up.sh"],capture_output=True, text=True)
    print(clean_up_result)
# NOTE: Input JSON cannot have any spaces in it
if __name__ == "__main__":
    raw_json = input()
    try:
        job_input_data = json.loads(raw_json)
    except:
        print("Error parsing json")
    job_sql_id = job_input_data["id"]
    job_basis_set = job_input_data["basisSet"]
    job_theory = job_input_data["theory"]
    job_wave_theory = job_input_data["waveTheory"]
    job_calculation_type = job_input_data["calculation"]
    job_solvent_effects = job_input_data["solventEffects"]
    script_path = "./" + job_sql_id
    write_sbatch_script(script_path, 'echo "test"')
    submit_sbatch_script(script_path)


