import json

from cancel_job import cancel_job
from check_status import check_status
from clean_result import clean_result
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
        parameters["root_dir"] = root_dir
    except Exception as error:
        log_error("Error parsing JSON: " + error, root_dir)
        # TODO: return something to the backend
    else:
        match action:
            case "submit":
                print(json.dumps(submit_job(parameters)))
            case "cancel":
                print(json.dumps(cancel_job(parameters)))
            case "upload":
                print(json.dumps(upload_result(parameters)))
            case "check":
                print(json.dumps(check_status(parameters)))
            case "clean":
                print(json.dumps(clean_result(parameters)))
            case _:
                log_error("Invalid action word: {action}", root_dir)
                # TODO: return something to the backend  
