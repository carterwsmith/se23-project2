import time, requests
from py_compile import compile
from os import listdir
from os.path import isfile, join

def check_py_syntax(F_PATH):
    py_paths = [f for f in listdir(F_PATH) if isfile(join(F_PATH, f)) and f.endswith('.py')]
    for py_path in py_paths:
        try:
            compile(py_path)
        except Exception as e:
            return False
    return True

def parse_github_payload(json):
    try:
        output = {}

        output['time'] = int(time.time())

        data = json["repository"]
        output['repo_name'] = data["name"]
        output['branch'] = json["ref"].split("/")[-1]
        output['owner_name'] = data["owner"]["name"]
        output['pusher_name'] = json["pusher"]["name"]
        output['url'] = data["owner"]["url"]
        output['clone_url'] = data["clone_url"]
        output['sha'] = json['after']

        return output
    except Exception as e:
        raise Exception("Error parsing GitHub payload: {}".format(e))

def change_commit_status(OWNER_NAME, REPO_NAME, SHA, STATUS):
    url = 'https://api.github.com/repos/'+OWNER_NAME+'/'+REPO_NAME+'/statuses/'+SHA
    if STATUS == "success": payload = {"state" : STATUS, "description" : "The build and tests succeeded."}
    else: payload = {"state" : STATUS, "description" : "The build or tests failed."}
    headers = {"Authorization" : "Bearer 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"}

    req = requests.post(url, json = payload, headers = headers)