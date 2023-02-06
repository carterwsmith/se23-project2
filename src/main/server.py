from flask import Flask, request
import json

app = Flask(__name__)
clone_dir = "./clone_dir"

@app.route("/", methods=["GET", "POST"])
def process_github_request():
    if "X-GitHub-Event" in request.headers:
        try:
            payload = request.json
            return payload
        except Exception as e:
            return "Error: {}".format(e)