import json
import subprocess
import sys

import requests

def fetch_result(file_path):
    command = f'cat {file_path}' 
    ssh_command = ["ssh cluster", command]
    
    try:
        result = subprocess.run(ssh_command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error fetching file: {e}")

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
    input_data = json.load(sys.stdin)
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
                print(json.dumps(fetch_result(result_path)))
            else:
                print(f"Upload failed with status code: {http_response.status_code}")
    except FileNotFoundError:
        print(f"Error: The file {result_path} does not exist.")
    except requests.RequestException as e:
        print(f"HTTP Request failed: {str(e)}")
