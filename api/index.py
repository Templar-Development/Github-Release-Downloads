import json
import re

import requests
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=["GET"])
def home():
    # get and render the index.html page
    
    page = "<main><h1>Github Release Stats</h1><hr><section><input type=\"text\" id=\"name\" placeholder=\"Github username\"><input type=\"text\" id=\"repo\" placeholder=\"Github repository\"><button id=\"trd\">Get Downloads</button><button id=\"ird\">Get Individual Downloads</button><button id=\"ldu\">Get Latest Download URL</button><button id=\"adu\">Get All Download URL\'s</button><p id=\"type\"></p><p id=\"result\"></p></section></main><script>const trd = document.getElementById('trd');const ird = document.getElementById('ird');const ldu = document.getElementById('ldu');const repo = document.getElementById('repo');const name = document.getElementById('name');trd.addEventListener(\"click\", function() {get(\"TRD\");document.getElementById('type').innerHTML = \"Total Download Amount\";});ird.addEventListener(\"click\", function() {get(\"IRD\");document.getElementById('type').innerHTML = \"Individual Download Amounts\";});ldu.addEventListener(\"click\", function() {get(\"LDU\");document.getElementById('type').innerHTML = \"Latest Download URL\";});adu.addEventListener(\"click\", function() {get(\"ADU\");document.getElementById('type').innerHTML = \"All Download URL's\";});const get = (type) => {const url = `https://github-release-downloads.vercel.app/${type}?user=${name.value}&repo=${repo.value}`;fetch(url).then((res) => res.text()).then((data) => {document.getElementById('result').innerHTML = data;});}</script>"
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