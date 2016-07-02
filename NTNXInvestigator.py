from flask import Flask, request, g, redirect, url_for, \
     session, render_template, flash

from json2html import *

import json
import sys
import requests
import datetime
import time

REST_URL_SUFFIX = 'https://%s:9440/PrismGateway/services/rest/v1'
base_url = REST_URL_SUFFIX


# Nutanix Who did What?  Name did Action

class NTNXEventRESTAPI():
    def __init__(self):
        self.session = requests.Session()

    def create_connection(self, username, password):
        # Creating REST client session for server connection
        self.session.auth = (username, password)
        self.session.verify = False
        self.session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
        return session

    def getEventsInformation(self, investigate_date):
        start_time = time.mktime(datetime.datetime.strptime(investigate_date, "%Y-%m-%d").timetuple())
        end_time = start_time + (24*60*60)
        start_time_url = str(int(start_time)) + "000000"
        end_time_url = str(int(end_time)) + "000000"
        eventsURL = base_url + "/events?" + "startTimeInUsecs=" + start_time_url + "&endTimeInUsecs=" + end_time_url
        serverResponse = self.session.get(eventsURL)
        json_events = json.loads(serverResponse.text)
        print json_events.keys()


        # list of alertType: ContainerAudit, RemoteSiteAudit, NFSDatastoreAudit, SnapshotReadyAudit,ReplicationSystemStateAudit,ProtectionDomainAudit
        # ProtectionDomainEntitiesAudit, PdCronScheduleAudit,ModifyProtectionDomainSnapshotAudit, ProtectionDomainChangeModeAudit, RegisterVmAudit


        def logininfo ():
            element.get('contextValues')[-1] = element.get('contextValues')[-1].replace('{audit_user}', element.get(
                    'contextValues')[0])
            element.get('contextValues')[-1] = element.get('contextValues')[-1].replace('{ip_address}', element.get(
                    'contextValues')[1])

        def containerinfo ():
            if element.get('contextValues')[-2].startswith("Updated"):
                    element.get('contextValues')[-2] = element.get('contextValues')[-2].replace('{container_name}',
                                                                                                element.get(
                                                                                                    'contextValues')[1])
            else:
                element.get('contextValues')[-2] = element.get('contextValues')[-2].replace('{container_name}',
                                                                                                element.get(
                                                                                                    'contextValues')[1])
                element.get('contextValues')[-2] = element.get('contextValues')[-2].replace('{storage_pool_name}',
                                                                                                element.get(
                                                                                                    'contextValues')[3])
        def datastoreinfo ():
            if element.get('contextValues')[-2].startswith("Creation"):
                element.get('contextValues')[-2] = element.get('contextValues')[-2].replace('{datastore_name}',
                                                                                            element.get(
                                                                                                'contextValues')[0])
                element.get('contextValues')[-2] = element.get('contextValues')[-2].replace('{container_name}',
                                                                                            element.get(
                                                                                                'contextValues')[1])

        event_types = {
            'LoginInfoAudit' : logininfo,
            'ContainerAudit' : containerinfo,
            'NFSDatastoreAudit': datastoreinfo,
        }

        for element in json_events['entities']:
            event_types[element.get('alertTypeUuid')]()

        return json_events


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '023aM47zz19Sx873yew9321Pl8746'


@app.route('/', methods=['GET', 'POST'])
def HomePage():
    error = None
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        username = request.form['username']
        password = request.form['password']
        global base_url
        base_url = REST_URL_SUFFIX%ip_address
        event_api_connection.create_connection(username, password)
        return redirect(url_for('querymainpage'))
    return render_template('homepage.html', error=error)


@app.route('/querymainpage', methods=['GET', 'POST'])
def querymainpage():
    error = None
    if request.method == 'POST':
        investigate_date = request.form['investigate_date']
        events = event_api_connection.getEventsInformation(investigate_date)
        return json2html.convert(json=events)
    return render_template('querymainpage.html', error=error)


if __name__ == '__main__':
    try:
        event_api_connection = NTNXEventRESTAPI()
        app.run()
    except Exception as ex:
        print ex
        sys.exit(1)
