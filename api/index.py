import json
import re

import requests
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=["GET"])
def home():
    page = "<h1>Github Release Stats</h1><p>End Points:</p><ul><li>TRD | Total release downloads</li><li>IRD | Individual release downloads</li><li>LDU | Latest download URL</li><li>ADU | All download URL's</li></ul><p>EX:</p><p>https://github-release-downloads.vercel.app/{type}?user={user}&repo={repo}</p>"
    return page

@app.route("/TRD", methods=['GET'])
def Repo_Total_Release_Downloads():
    args = request.args
    user = args.get("user", default="", type=str)
    repo = args.get("repo", default="", type=str)

    url = "https://api.github.com/repos/{}/{}/releases".format(user, repo)
    response = requests.get(url)
    response = response.json()

    total_Downloads = 0

    for i in response:
        if isinstance(i['assets'][0], dict):
            total_Downloads += i['assets'][0]['download_count']

    print(f'Requested: {user}/{repo} | Total Downloads: {total_Downloads}')

    return str(total_Downloads)

@app.route("/IRD", methods=['GET'])
def Repo_Individual_Release_Downloads():
    args = request.args
    user = args.get("user", default="", type=str)
    repo = args.get("repo", default="", type=str)

    url = "https://api.github.com/repos/{}/{}/releases".format(user, repo)
    response = requests.get(url)
    response = response.json()
    
    individual_Downloads = []
    
    for i in response:
        individual_Downloads.append(i['assets'][0]['download_count'])

    print(f'Requested: {user}/{repo} | Individual Downloads: {individual_Downloads}')
        
    return str(individual_Downloads)

@app.route("/LDU", methods=['GET'])
def Latest_Download_URL():
    args = request.args
    user = args.get("user", default="", type=str)
    repo = args.get("repo", default="", type=str)

    url = "https://api.github.com/repos/{}/{}/releases/latest".format(user, repo)
    response = requests.get(url)
    response = response.json()
    
    download_url = response['assets'][0]['browser_download_url']

    print(f'Requested: {user}/{repo} | Latest Download URL: {download_url}')
        
    return str(download_url)

@app.route("/ADU", methods=['GET'])
def All_Download_URLs():
    args = request.args
    user = args.get("user", default="", type=str)
    repo = args.get("repo", default="", type=str)

    url = "https://api.github.com/repos/{}/{}/releases".format(user, repo)
    response = requests.get(url)
    response = response.json()
    
    download_urls = []
    
    for i in response:
        download_url = (i['assets'][0]['browser_download_url'])
        download_name = (i['name'])
        download_details = (download_name, download_url)
        download_urls.append(download_details)

    print(f'Requested: {user}/{repo} | All Download URLs: {download_urls}')
    
    download_urls = json.dumps(download_urls)
        
    return download_urls

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)