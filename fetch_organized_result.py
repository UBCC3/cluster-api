import base64
import json
import subprocess
import sys

import requests

def fetch_result(file_path):
    command = ["cat", file_path]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error: {e}")

if __name__ == "__main__":
    """
    Sample input:
    {
        "JobID": "samplejobid",
        "PresignedResponse": 
            {
                ... 
            }
    }
    - the "..." refer to the response from create_presigned_post() in backend
    """
    json_data = base64.b64decode(sys.stdin).decode('utf-8')
    input_data = json.loads(json_data)
    db_job_id = input_data["JobID"]
    presigned_response = input_data["PresignedResponse"]
    # TODO: update with the actual file path
    result_path = f'/ubchemica/{db_job_id}/{db_job_id}.json'
    try:
        with open(result_path, 'rb') as f:
            files = {'file': (result_path, f)}
            http_response = requests.post(presigned_response['url'], 
                                          data=presigned_response['fields'], 
                                          files=files)
            if http_response.status_code == 204:
                return_data = {"status_code": http_response.status_code, "output": fetch_result(result_path)}
                return_json = json.dumps(return_data)
                return_encoded_json = base64.b64encode(return_json.encode()).decode('utf-8')
                print(json.dumps(return_encoded_json))
            else:
                return_data = {"status_code": http_response.status_code}
                return_json = json.dumps(return_data)
                return_encoded_json = base64.b64encode(return_json.encode()).decode('utf-8')
                print(json.dumps(return_encoded_json))
    except requests.RequestException as e:
        error_message = f'HTTP request fail with {str(e)}'
        return_json = json.dumps({"Error": error_message})
        return_encoded_json = base64.b64encode(return_json.encode()).decode('utf-8')
        print(json.dumps(return_encoded_json))
    except Exception as e:
        return_json = json.dumps({"Error": str(e)})
        return_encoded_json = base64.b64encode(return_json.encode()).decode('utf-8')
        print(json.dumps(return_encoded_json))
        