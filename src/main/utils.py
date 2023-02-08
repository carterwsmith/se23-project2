"""
This Python file implements the utility functions which are essential for the 3 core features of the
CI server.
"""

import time, requests
from dotenv import load_dotenv, find_dotenv
from py_compile import compile
from os import listdir, getenv
from os.path import isfile, join


"""
This function iterates through a directory to find all .py files and try to compile them. If all python files
had correct systax, the function would return True. Otherwise, the function throws an exception and returns False. 
@param1 F_PATH the path of the directory which contains the .py files we need to check 
@return True if all python files can be successfully compiled, otherwise False
"""
def check_py_syntax(F_PATH):
    py_paths = [f for f in listdir(F_PATH) if isfile(join(F_PATH, f)) and f.endswith('.py')]
    for py_path in py_paths:
        try:
            compile(py_path)
        except Exception as e:
            return False
    return True


"""
This function takes json payload as input, and trys to retrieve the needed information into a dictionary. 
It raises an exception if the data extraction fails. 
@param1 json payload sent by github, which contains essential webhook information
@return output is a dictionary which contains the necessary information retrieved from json payload
"""
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


"""
This function takes 
@param1 OWNER_NAME the name of the repository owner
@param2 REPO_NAME the name of the repository
@param3 SHA the exclusive sha for each commit
@param4 STATUS the commit status we need to change
"""
def change_commit_status(OWNER_NAME, REPO_NAME, SHA, STATUS):
    load_dotenv(find_dotenv())
    TOKEN = getenv("GITHUB_ACCESS_TOKEN")

    url = 'https://api.github.com/repos/'+OWNER_NAME+'/'+REPO_NAME+'/statuses/'+SHA
    if STATUS == "success": payload = {"state" : STATUS, "description" : "The build and tests succeeded."}
    else: payload = {"state" : STATUS, "description" : "The build or tests failed."}
    headers = {"Authorization" : f"token {TOKEN}"}

    req = requests.post(url, json = payload, headers = headers)