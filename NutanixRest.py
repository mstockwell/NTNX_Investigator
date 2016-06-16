#!/usr/bin/env python
#
# NOTE: You need a Python library called "requests" which can be available from
# the url: http://docs.python-requests.org/en/latest/user/install/#install

#setup with VENV virtualenvironment  Remember to start venv  . venv/bin/activate

from flask import Flask

import json
import pprint
import sys

import requests


class TestRestApi():
    def __init__(self):
        # Initializes the options and the logfile from GFLAGS.
        self.serverIpAddress = "10.20.26.11"
        self.username = "mel.stockwe@nutanixdc.local"
        self.password = "giant29Er"
        # Base URL at which REST services are hosted in Prism Gateway.
        BASE_URL = 'https://%s:9440/PrismGateway/services/rest/v1/'
        self.base_url = BASE_URL % self.serverIpAddress
        self.session = self.get_server_session(self.username, self.password)

    def get_server_session(self, username, password):
        # Creating REST client session for server connection, after globally setting
        # Authorization, content type, and character set for the session.
        session = requests.Session()
        session.auth = (username, password)
        session.verify = False
        session.headers.update(
            {'Content-Type': 'application/json; charset=utf-8'})
        return session

    # Prints the cluster information and loads JSON objects to be formatted.

    def getClusterInformation(self):
        # This sets up 'pretty print' for the object.
        pp = pprint.PrettyPrinter(indent=2)
        clusterURL = self.base_url + "/cluster"
        print "Getting cluster information for cluster %s" % self.serverIpAddress
        serverResponse = self.session.get(clusterURL)
        print "Response code: %s" % serverResponse.status_code
        return serverResponse.status_code, json.loads(serverResponse.text)

    def getHostsInformation(self):
        # This sets up 'pretty print' for the object.
        pp = pprint.PrettyPrinter(indent=2)
        HostsURL = self.base_url + "/hosts/00051dd5-8993-5496-0000-000000004c2a::10"
        print "Getting Hosts information for cluster %s" % self.serverIpAddress
        serverResponse = self.session.get(HostsURL)
        print "Response code: %s" % serverResponse.status_code
        return serverResponse.status_code, json.loads(serverResponse.text)


app = Flask(__name__)

@app.route('/')
def hello_world():
    status, c = testRestApi.getClusterInformation()
    return "Cluster is %s" % c.get('name')

if __name__ == "__main__":
    try:
        # Set the Pretty Printer variable to format data.
        pp = pprint.PrettyPrinter(indent=2)

        # Start the execution of test cases.
        testRestApi = TestRestApi()
        print ("=" * 79)
        status, cluster = testRestApi.getClusterInformation()
        status, hosts = testRestApi.getHostsInformation()
        print ("=" * 79)
        clustername = cluster.get('name')
        # Displays cluster authentication response and information.
        print "Status code: %s" % status
        print "Text: "  # %s" % cluster
        print "Text: "  # %s % hosts
        #    pp.pprint(cluster)
        print "Break"
        pp.pprint(hosts)
        print ("=" * 79)

        # Get specific cluster elements.
        print "Host state: %s" % hosts.get('state')
        print "Host Model: %s" % hosts.get('model')
        print "Name: %s" % cluster.get('name')
        print "ID: %s" % cluster.get('id')
        print "Cluster External IP Address: %s" % cluster.get('clusterExternalIPAddress')
        print "Number of Nodes: %s" % cluster.get('numNodes')
        print "Version: %s" % cluster.get('version')
        print ("=" * 79)
        app.run()
    except Exception as ex:
        print ex
        sys.exit(1)
