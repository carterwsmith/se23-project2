"""
Implements the server with 3 core features and 1 optional feature for P+:
1. Complies the group project, a static syntax check is to be performed for languages without compiler.
Compilation is triggered as webhook, the CI server compiles the branch  where the change has been made.
2. Executes the automated tests of the group project. Testing is triggered as webhook, on the branch
where the change has been made.
3. Notify CI results by changing the commit status
P+ feature: Keep the history of past builds
"""

from flask import Flask, make_response, request, jsonify
from git import Repo, rmtree
import json, os, shutil, subprocess, pytest, sys, traceback

from utils import parse_github_payload, check_py_syntax, change_commit_status, store_ci_result

app = Flask(__name__)
CLONE_DIR = "./tmp/"
HISTORY_DIR = "./history"
HISTORY_FILE = "ci.history"


@app.route("/history", methods=["GET"])
def show_ci_history():
    """
    This function implements the <url>/history page, which shows the results of
    CI jobs the server has performed.
    @return http response 200 with the history on record
            or http response 400 if there is none
    """
    try:
        with open(HISTORY_DIR + "/" + HISTORY_FILE, "r", encoding="utf-8") as f:
            records = f.readlines()
            vis = "<br/>".join(records)
            return make_response(vis, 200)
    except OSError:  # file doesn't exist
        return make_response("No history available", 400)


@app.route("/history/<hash>", methods=["GET"])
def show_job_info(hash):
    """
    This funciton loads the ci info of a specific job given by the hash.
    @param1 hash the hash/filename of a job.
    @return http response 200 with the info of this job as an HTML string
            or http response 404 if the server has no record of this job
    """
    try:
        with open(HISTORY_DIR + f"/{hash}", "r", encoding="utf-8") as f:
            page = f.readlines()
            return make_response("\n".join(page), 200)
    except OSError:
        return make_response("Job not found", 404)



@app.route("/", methods=["GET", "POST"])
def process_github_request():
    """
    The function implements the core features of the CI server utilizing functions from utils.py. It first retrieves
    the URL of the repo and clone it to a local directory. Then, it trys to check the syntax of all .py files, run
    the automated test, and change the corresponding commit status. It also keeps the build history.
    @return http response 200 based on the corresponding github event (push or ping)
    http response 404 if the request is not from github
    """
    if "X-GitHub-Event" in request.headers and request.headers["X-GitHub-Event"] == "push":
        try:
            # Remove temp directory if it exists already, in which we need to store the cloned repo
            if os.path.exists(CLONE_DIR):
                rmtree(CLONE_DIR)

            # Retrieve necessary data from json payload
            payload_data = parse_github_payload(request.json)
            COMMIT_BRANCH = payload_data["branch"]
            CLONE_URL = payload_data["clone_url"]

            # Clone the repository
            Repo.clone_from(
                CLONE_URL, CLONE_DIR, branch=COMMIT_BRANCH
            )

            # Change commit status to pending when building and testing
            change_commit_status(OWNER_NAME=payload_data["owner_name"],
                                 REPO_NAME=payload_data["repo_name"],
                                 SHA=payload_data["sha"],
                                 STATUS="pending")

            # Compile and check syntax of all .py files in the cloned directory
            SYNTAX_CHECK = check_py_syntax(F_PATH=CLONE_DIR)
            TMP_TEST_PATH = CLONE_DIR + "src/test"

            # Invoke tests with subprocess and get result of the tests
            test_output = subprocess.run(["python", "-m", "pytest", TMP_TEST_PATH], capture_output=True)
            test_logs = test_output.stdout.decode("utf-8")
            TEST_RESULT = False
            if "passed" in test_logs and "failed" not in test_logs:
                TEST_RESULT = True

            # Remove temp directory when done
            rmtree(CLONE_DIR)

            # Change the commit status according to syntax check and test result
            conditions = [SYNTAX_CHECK, TEST_RESULT]
            if all(conditions):
                STATUS = "success"
            else:
                STATUS = "failure"
            change_commit_status(OWNER_NAME=payload_data["owner_name"],
                                 REPO_NAME=payload_data["repo_name"],
                                 SHA=payload_data["sha"],
                                 STATUS=STATUS)

            # store build history
            store_ci_result(HISTORY_DIR, HISTORY_FILE, request.json, test_logs, STATUS)

            return make_response(jsonify(payload_data), 200)
        except Exception as e:
            return "Error: {}".format(traceback.format_exc())
    elif "X-GitHub-Event" in request.headers and request.headers["X-GitHub-Event"] == "ping":
        return make_response("GitHub ping successful", 200)
    else:
        return make_response("Not a GitHub request", 404)
