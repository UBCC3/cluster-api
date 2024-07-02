import os

from main import root_dir
from util import clean_up

def clean_result(parameters):
    db_job_id = parameters["JobID"]
    file_path = os.path.join(root_dir, db_job_id)
    if clean_up(file_path):
        return "{'status':'SUCCESS'}"
    else:
        return "{'status':'FAILURE'}"
    