import os

import requests

from util import log_error

def upload_result(parameters):
    """
    Upload files directly to the S3 bucket using AWS presigned URLs
    Input:
        - parameters: a dictionary that contains:
            - Type: the type of file to be uploaded (zip or json)
            - JobID: job ID in the database
            - PresignedResponse: the presigned URL with any required fields for the POST request
            - root_dir: the root directory path
    Output:
        - A dictionary that contains the HTTP status code of the upload request
    """
    root_dir = parameters["root_dir"]
    result_type = ""
    if parameters["Type"] == "zip":
        result_type = ".zip"
    elif parameters["Type"] == "json":
        result_type = ".json"
    else:
        log_error(f'Invalid Type word: {parameters["Type"]}', root_dir)
        # TODO: return something to the backend
    db_job_id = parameters["JobID"]
    presigned_response = parameters["PresignedResponse"]
    job_dir = os.path.join(root_dir, db_job_id, f'{db_job_id}{result_type}')
    try:
        with open(job_dir, 'rb') as f:
            files = {'file': (job_dir, f)}
            http_response = requests.post(presigned_response['url'], 
                                          data=presigned_response['fields'], 
                                          files=files)
            return {"status_code": http_response.status_code}
    except requests.RequestException as e:
        log_error(f'HTTP request fail with {str(e)}', root_dir)
        # TODO: return something to the backend
    except Exception as e:
        log_error(f'Error {str(e)}', root_dir)
        # TODO: return something to the backend
