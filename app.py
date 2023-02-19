import json
import re

import requests
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=["GET"])
def home():
    return "<h1>GIthub Downloads API.</h1>"


@app.route("/TD", methods=['GET'])
def Whitaker_Latin_To_English():
    args = request.args
    user = args.get("user", default="", type=str)
    repo = args.get("repo", default="", type=str)

    url = "https://api.github.com/repos/{}/{}/releases".format(user, repo)
    response = requests.get(url)
    response = response.json()
    
    total_Downloads = 0
    
    for i in response:
        total_Downloads += i['assets'][0]['download_count']

    print(f'Requested: {user}/{repo} | Total Downloads: {total_Downloads}')
        
    return str(total_Downloads)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)