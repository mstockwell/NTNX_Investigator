from flask import session
import requests
import sys
import datetime
import time
import json

REST_URL_SUFFIX = 'https://%s:9440/PrismGateway/services/rest/v1'
my_session = requests.Session()


def test_credentials(username, password, ip_address):
    session['ip_address'] = ip_address
    base_url = REST_URL_SUFFIX%session['ip_address']
    my_session.auth = (username, password)
    my_session.verify = False
    my_session.headers.update({'Content-Type': 'application/json; charset=utf-8'})

    try:
        serverResponse = my_session.get(base_url + "/cluster", timeout=10)
        return serverResponse
    except:
        print "Nutant, we have a problem!"


def get_events_data(investigate_date):
    # RemoteSiteAudit, SnapshotReadyAudit,ReplicationSystemStateAudit,ProtectionDomainAudit
    # ProtectionDomainEntitiesAudit, PdCronScheduleAudit,ModifyProtectionDomainSnapshotAudit,
    # ProtectionDomainChangeModeAudit, RegisterVmAudit

    def create_event_rest_url(date):
        start_time = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
        end_time = start_time + (24*60*60)
        start_time_url = str(int(start_time)) + "000000"
        end_time_url = str(int(end_time)) + "000000"
        base_url = REST_URL_SUFFIX%session['ip_address']
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
    serverResponse = my_session.get(eventsURL)
    json_events = json.loads(serverResponse.text)
    event_list = []
    for element in json_events['entities']:
        # print element.get('alertTypeUuid')
        event_user, event_msg = event_types[element.get('alertTypeUuid')]()
        event_list.append((event_user, event_msg))
    for x in event_list: print x
    # return json_events
    return event_list


from NTNXWhoDidWhat import app

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as ex:
        print ex
        sys.exit(1)
