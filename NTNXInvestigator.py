from flask import Flask, request, g, redirect, url_for, \
    abort, session, render_template, flash

import json
import sys
import requests

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
        ipaddress=request.form['ipaddress']
        username = request.form['username']
        password = request.form['password']
        BASE_URL = 'https://%s:9440/PrismGateway/services/rest/v1/'
        global base_url
        base_url = BASE_URL % ipaddress
        connection = requests.Session()
        connection.auth = (username, password)
        connection.verify = False
        connection.headers.update({'Content-Type': 'application/json; charset=utf-8'})
        clusterURL = base_url + "/cluster"
        ServerResponse = connection.get(clusterURL)
        return "Response Code %s" % json.loads(ServerResponse.text)
    return render_template('login.html', error=error)


@app.route('/cluster')
def cluster_info():
    # BASE_URL = 'https://%s:9440/PrismGateway/services/rest/v1/'
    # base_url = BASE_URL % ipaddress
    print "This is the base_url %s" % base_url
    clusterURL = base_url + "/cluster"
    serverResponse = session.get(clusterURL)
    jsonload = json.loads(serverResponse.text)
    return "<h2> Cluster Name: %s <h2>" % jsonload.get('name')


if __name__ == '__main__':
    try:
        app.run()
    except Exception as ex:
        print ex
        sys.exit(1)
