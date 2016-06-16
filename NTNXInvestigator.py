from flask import Flask, request, g, redirect, url_for, \
    abort, session, render_template, flash

import json
import sys
import requests

REST_URL_SUFFIX = 'https://%s:9440/PrismGateway/services/rest/v1/'
base_url = REST_URL_SUFFIX

class RestConnection():
    def __init__(self):
        self.session = requests.Session()

    def create_connection (self, username, password):
        # Creating REST client session for server connection
        self.session.auth = (username, password)
        self.session.verify = False
        self.session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
        return session

    def getClusterInformation(self):
        clusterURL = base_url + "/cluster"
        serverResponse = self.session.get(clusterURL)
        return json.loads(serverResponse.text)

# create application
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '0234719873yew93218746'


@app.route('/')
def HomePage():
    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        username = request.form['username']
        password = request.form['password']
        global base_url
        base_url = REST_URL_SUFFIX % ip_address
        rc.create_connection(username, password)
        return "Status %s" % rc.__class__
    return render_template('login.html', error=error)


@app.route('/cluster')
def cluster_info():
    cluster = rc.getClusterInformation()
    return "Cluster Name: %s" % cluster.get('name')


if __name__ == '__main__':
    try:
        rc = RestConnection()
        app.run()
    except Exception as ex:
        print ex
        sys.exit(1)
