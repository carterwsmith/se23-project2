from flask import Flask, make_response, request, jsonify
from git import Repo
import json

app = Flask(__name__)
clone_dir = "./clone_dir"

@app.route("/", methods=["GET", "POST"])
def process_github_request():
    if "X-GitHub-Event" in request.headers and request.headers["X-GitHub-Event"] == "push":
        try:
            payload = request.json
            return payload
        except Exception as e:
            return "Error: {}".format(e)
    elif "X-GitHub-Event" in request.headers and request.headers["X-GitHub-Event"] == "ping":
        return make_response("GitHub ping successful", 200)
    else:
        return make_response("Not a GitHub request", 404)