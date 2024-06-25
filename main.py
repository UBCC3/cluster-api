import sys
import json
from submit_job import submit_job
from cancel_job import cancel_job
if __name__ == "__main__":
    raw_json = input()
    try:
        job_input_data = json.loads(raw_json)
        action = job_input_data["action"]
    except:
        print("Error parsing JSON")
    match action:
        case "submit":
            submit_job(job_input_data)
        case "cancel":
            cancel_job(job_input_data)
        case "fetch":
            pass
        case "check":
            pass
        case _:
            raise Exception("Invalid action word: {action}") 