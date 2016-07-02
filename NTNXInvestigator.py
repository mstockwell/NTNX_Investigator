from flask import Flask, request, g, redirect, url_for, \
    session, render_template

from json2html import *

import json
import sys
import requests
import datetime
import time

REST_URL_SUFFIX = 'https://%s:9440/PrismGateway/services/rest/v1'
base_url = REST_URL_SUFFIX


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

        # RemoteSiteAudit, SnapshotReadyAudit,ReplicationSystemStateAudit,ProtectionDomainAudit
        # ProtectionDomainEntitiesAudit, PdCronScheduleAudit,ModifyProtectionDomainSnapshotAudit, ProtectionDomainChangeModeAudit, RegisterVmAudit

        def create_event_rest_url(date):
            start_time = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
            end_time = start_time + (24*60*60)
            start_time_url = str(int(start_time)) + "000000"
            end_time_url = str(int(end_time)) + "000000"
            url = base_url + "/events?" + "startTimeInUsecs=" + start_time_url + "&endTimeInUsecs=" + end_time_url
            return url

        def login_event():
            user_info = element.get('contextValues')[0]
            event_info = element.get('contextValues')[-1].replace('{audit_user}', element.get(
                'contextValues')[0])
            event_info = event_info.replace('{ip_address}', element.get(
                'contextValues')[1])
            return user_info, event_info

        def container_event():
            user_info = element.get('contextValues')[-1]
            event_info = element.get('contextValues')[-2].replace('{container_name}', element.get('contextValues')[1])
            if event_info.startswith("Added"):
                event_info = event_info.replace('{storage_pool_name}', element.get('contextValues')[3])
            return user_info, event_info

        def nfs_datastore_event():
            user_info = element.get('contextValues')[-1]
            if element.get('contextValues')[-2].startswith("Creation"):
                event_info = element.get('contextValues')[-2].replace('{datastore_name}',
                                                                      element.get('contextValues')[0])
                event_info = event_info.replace('{container_name}', element.get('contextValues')[1])
            else:
                event_info = "datastore update event"
            return user_info, event_info

        event_types = {
            'LoginInfoAudit': login_event,
            'ContainerAudit': container_event,
            'NFSDatastoreAudit': nfs_datastore_event,
        }

        eventsURL = create_event_rest_url(investigate_date)
        serverResponse = self.session.get(eventsURL)
        json_events = json.loads(serverResponse.text)
        event_list = []
        for element in json_events['entities']:
            # print element.get('alertTypeUuid')
            event_user, event_msg = event_types[element.get('alertTypeUuid')]()
            event_list.append((event_user, event_msg))
        for x in event_list: print x
        # return json_events
        return event_list


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
        return render_template('results.html', num_events=len(events),events_list=events, investigate_date=investigate_date)
        # return json2html.convert(json=events)
    return render_template('querymainpage.html', error=error)


if __name__ == '__main__':
    try:
        event_api_connection = NTNXEventRESTAPI()
        app.run(debug=True)
    except Exception as ex:
        print ex
        sys.exit(1)
