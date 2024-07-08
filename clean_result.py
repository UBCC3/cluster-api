import os

from util import clean_up

def clean_result(parameters):
    db_job_id = parameters["id"]
    root_dir = parameters["root_dir"]
    job_dir = os.path.join(root_dir, db_job_id)
    if clean_up(job_dir):
        return "{'status':'SUCCESS'}"
    else:
        return "{'status':'FAILURE'}"
    
