import os

from main import root_dir
from util import clean_up

def clean_result(parameters):
    db_job_id = parameters["JobID"]
    root_dir = parameters["root_dir"]
    file_path = os.path.join(root_dir, db_job_id)
    clean_up(file_path)
    