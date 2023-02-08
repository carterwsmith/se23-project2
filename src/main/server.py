"""
Implements the server with 3 core features:
1. Complies the group project, a static syntax check is to be performed for languages without compiler.
Compilation is triggered as webhook, the CI server compiles the branch  where the change has been made.
2. Executes the automated tests of the group project. Testing is triggered as webhook, on the branch
where the change has been made.
3. Notify CI results by changing the commit status

"""

from flask import Flask, make_response, request, jsonify
from git import Repo
import json, os, shutil, subprocess, pytest, traceback

from utils import parse_github_payload, check_py_syntax, change_commit_status

app = Flask(__name__)
CLONE_DIR = "./tmp/"


"""
The function implements the core features of the CI server utilizing functions from utils.py. It first retrieves
the URL of the repo and clone it to a local directory. Then, it trys to check the syntax of all .py files, run 
the automated test, and change the corresponding commit status. 
@return http response 200 based on the corresponding github event (push or ping)
http response 404 if the request is not from github
"""
@app.route("/", methods=["GET", "POST"])
def process_github_request():
    if "X-GitHub-Event" in request.headers and request.headers["X-GitHub-Event"] == "push":
        try:
            # Remove temp directory if it exists already, in which we need to store the cloned repo
            if os.path.exists(CLONE_DIR): shutil.rmtree(CLONE_DIR)

            # Retrieve necessary data from json payload
            payload_data = parse_github_payload(request.json)
            COMMIT_BRANCH = payload_data["branch"]
            CLONE_URL = payload_data["clone_url"]

            # Clone the repository
            Repo.clone_from(
                CLONE_URL, CLONE_DIR, branch=COMMIT_BRANCH
            )

            # Compile and check syntax of all .py files in the cloned directory
            SYNTAX_CHECK = check_py_syntax(F_PATH=CLONE_DIR)

            # Invoke tests with subprocess and get result of the tests
            tmp_test_path = CLONE_DIR + "src/test"
            test_output = subprocess.run(["python3", "-m", "pytest", tmp_test_path], capture_output=True)
            TEST_RESULT = False
            if "passed" in test_output.stdout.decode("utf-8") and "failed" not in test_output.stdout.decode("utf-8"):
                TEST_RESULT = True

            # Remove temp directory when done
            shutil.rmtree(CLONE_DIR)

            # Change the commit status according to syntax check and test result
            conditions = [SYNTAX_CHECK, TEST_RESULT]
            if all(conditions): STATUS = "success"
            else: STATUS = "failure"
            change_commit_status(OWNER_NAME=payload_data["owner_name"], 
                                REPO_NAME=payload_data["repo_name"], 
                                SHA=payload_data["sha"], 
                                STATUS=STATUS)

            return make_response(jsonify(payload_data), 200)
        except Exception as e:
            return "Error: {}".format(traceback.format_exc())
    elif "X-GitHub-Event" in request.headers and request.headers["X-GitHub-Event"] == "ping":
        return make_response("GitHub ping successful", 200)
    else:
        return make_response("Not a GitHub request", 404)