from flask import Flask, make_response, request, jsonify
from git import Repo
import json, os, shutil, pytest

from utils import parse_github_payload

app = Flask(__name__)
CLONE_DIR = "./tmp/"

@app.route("/", methods=["GET", "POST"])
def process_github_request():
    if "X-GitHub-Event" in request.headers and request.headers["X-GitHub-Event"] == "push":
        try:
            # Remove temp directory if it exists already
            if os.path.exists(CLONE_DIR): shutil.rmtree(CLONE_DIR)

            payload_data = parse_github_payload(request.json)

            COMMIT_BRANCH = payload_data["branch"]
            CLONE_URL = payload_data["clone_url"]
            
            Repo.clone_from(
                CLONE_URL, CLONE_DIR, branch=COMMIT_BRANCH
            )

            pytest_args = [
                './tmp/src/test',
            ]
            TEST_CODE = pytest.main(pytest_args)
            TEST_RESULT = True if TEST_CODE == pytest.ExitCode.OK else False

            # Remove temp directory when done
            shutil.rmtree(CLONE_DIR)
            
            return make_response(jsonify(payload_data), 200)
        except Exception as e:
            return "Error: {}".format(e)
    elif "X-GitHub-Event" in request.headers and request.headers["X-GitHub-Event"] == "ping":
        return make_response("GitHub ping successful", 200)
    else:
        return make_response("Not a GitHub request", 404)