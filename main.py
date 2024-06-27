import json

from cancel_job import cancel_job
from check_status import check_status
from upload_result import upload_result
from submit_job import submit_job
from util import log_error

root_dir = "."

if __name__ == "__main__":
    raw_json = input()
    try:
        job_input_data = json.loads(raw_json)
        action = job_input_data["action"]
        parameters = job_input_data["parameters"]
    except:
        log_error("Error parsing JSON")
    match action:
        case "submit":
            submit_job(parameters)
        case "cancel":
            cancel_job(parameters)
        case "upload":
            upload_result(parameters)
        case "check":
            check_status(parameters)
        case _:
            log_error("Invalid action word: {action}")