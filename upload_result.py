import json
import os

import requests

from main import root_dir
from util import log_error

def upload_result(parameters):
    result_type = ""
    if parameters["Type"] == "zip":
        result_type = ".zip"
    elif parameters["Type"] == "json":
        result_type = ".json"
    else:
        log_error(f'Invalid Type word: {parameters["Type"]}')
    db_job_id = parameters["JobID"]
    presigned_response = parameters["PresignedResponse"]
    result_path = os.path.join(root_dir, db_job_id, f'{db_job_id}{result_type}')
    try:
        with open(result_path, 'rb') as f:
            files = {'file': (result_path, f)}
            http_response = requests.post(presigned_response['url'], 
                                          data=presigned_response['fields'], 
                                          files=files)
            return_data = {"status_code": http_response.status_code}
            print(json.dumps(return_data))
    except requests.RequestException as e:
        log_error(f'HTTP request fail with {str(e)}')
    except Exception as e:
        log_error(f'Error {str(e)}')
