import time

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

        return output
    except Exception as e:
        raise Exception("Error parsing GitHub payload: {}".format(e))