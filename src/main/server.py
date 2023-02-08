from flask import Flask, make_response, request, jsonify
from git import Repo, rmtree
import json, os, shutil, subprocess, pytest, traceback

from utils import parse_github_payload, check_py_syntax, change_commit_status

app = Flask(__name__)
CLONE_DIR = "./tmp/"
HISTORY_FILE = "./ci.history"


@app.route("/", methods=["GET", "POST"])
def process_github_request():
    if "X-GitHub-Event" in request.headers and request.headers["X-GitHub-Event"] == "push":
        try:
            # Remove temp directory if it exists already
            if os.path.exists(CLONE_DIR):
                rmtree(CLONE_DIR)

            payload_data = parse_github_payload(request.json)

            COMMIT_BRANCH = payload_data["branch"]
            CLONE_URL = payload_data["clone_url"]

            Repo.clone_from(
                CLONE_URL, CLONE_DIR, branch=COMMIT_BRANCH
            )

            print(f"LOG: Cloned repository: {CLONE_URL}/{COMMIT_BRANCH}", flush=True)

            # Compile and check syntax of all .py files in the cloned directory
            SYNTAX_CHECK = check_py_syntax(F_PATH=CLONE_DIR)

            print(f"LOG: Checked syntax. Success: {SYNTAX_CHECK}")

            # Invoke tests with subprocess
            tmp_test_path = CLONE_DIR + "src/test"
            test_output = subprocess.run(["python3", "-m", "pytest", tmp_test_path], capture_output=True)
            TEST_RESULT = False
            if "passed" in test_output.stdout.decode("utf-8") and "failed" not in test_output.stdout.decode("utf-8"):
                TEST_RESULT = True

            print(f"LOG: Ran tests. Output: {test_output.stdout.decode('utf-8')}", flush=True)

            # Remove temp directory when done
            rmtree(CLONE_DIR)

            conditions = [SYNTAX_CHECK, TEST_RESULT]
            if all(conditions):
                STATUS = "success"
            else:
                STATUS = "failure"
            print("LOG: Attempting to change commit status...", flush=True)
            change_commit_status(OWNER_NAME=payload_data["owner_name"],
                                 REPO_NAME=payload_data["repo_name"],
                                 SHA=payload_data["sha"],
                                 STATUS=STATUS)
            print(f"LOG: Changed commit status to: {STATUS}", flush=True)

            return make_response(jsonify(payload_data), 200)
        except Exception as e:
            return "Error: {}".format(traceback.format_exc())
    elif "X-GitHub-Event" in request.headers and request.headers["X-GitHub-Event"] == "ping":
        return make_response("GitHub ping successful", 200)
    else:
        return make_response("Not a GitHub request", 404)
