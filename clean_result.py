import os

from main import root_dir
from util import clean_up

def clean_result(parameters):
    db_job_id = parameters["JobID"]
    file_path = os.path.join(root_dir, db_job_id)
    clean_up(file_path)
    