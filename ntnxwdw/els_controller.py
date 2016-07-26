from flask import session, Flask
import requests
import datetime
import time
import json

REST_URL_SUFFIX = 'https://%s:9440/PrismGateway/services/rest/v1'
my_session = requests.Session()
requests.packages.urllib3.disable_warnings()


def test_credentials(username, password, ip_address):
    session['ip_address'] = ip_address
    session['username'] = username
    session['password'] = password
    base_url = REST_URL_SUFFIX%ip_address
    my_session.auth = (username, password)
    my_session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
    serverResponse = my_session.get(base_url + "/cluster", timeout=20, verify=False)
    return serverResponse.status_code, json.loads(serverResponse.text)


class NutanixEvents(object):
    def get_events(self, search_date):

        rest_session = requests.Session()
        rest_session.auth = (session['username'], session['password'])
        rest_session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
        # Set the date to retrieve events from Nutanix Cluster
        eventsURL = self.set_event_url(search_date)

        # Call the Acropolis REST API for Events
        serverResponse = rest_session.get(eventsURL, timeout=20, verify=False)

        # Load response from Nutanix Cluster into JSON object and then create list of events with account id,
        # event message, and time of event.  Also create list of unique account ids for filtering functions
        json_events = json.loads(serverResponse.text)

        event_list = []
        unique_accounts = set()
        for element in json_events['entities']:
            event_time = time.localtime(element.get('createdTimeStampInUsecs')/1000000)
            try:
                method_name = element.get('alertTypeUuid')
                # Get the method from 'self'. Default to a lambda.
                method = getattr(self, method_name, lambda: "nothing")
                # Call the method as we return it
                event_user, event_msg = method(element)
            except KeyError:
                event_user = "Unknown"
                event_msg = "An event not captured by Nutanix ELS"
            event_list.append((event_user, event_msg, time.strftime('%I:%M:%S %p %Z', event_time)))
            unique_accounts.add(event_user)
        event_list.sort(key=lambda tup: tup[2])
        return list(unique_accounts), event_list

    @staticmethod
    def set_event_url(search_date):
        REST_SUFFIX = 'https://%s:9440/PrismGateway/services/rest/v1'
        start_time = time.mktime(datetime.datetime.strptime(search_date, "%Y-%m-%d").timetuple())
        end_time = start_time + (24*60*60)
        start_time_url = str(int(start_time)) + "000000"
        end_time_url = str(int(end_time)) + "000000"
        base_url = REST_SUFFIX%session['ip_address']
        url = base_url + "/events?" + "startTimeInUsecs=" + start_time_url + "&endTimeInUsecs=" + end_time_url
        return url

    @staticmethod
    def LoginInfoAudit(element):
        user_info = element.get('contextValues')[0]
        event_info = element.get('contextValues')[-1].replace('{audit_user}', element.get(
            'contextValues')[0])
        event_info = event_info.replace('{ip_address}', element.get(
            'contextValues')[1])
        return user_info, event_info

    @staticmethod
    def ContainerAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[-2].replace('{container_name}', element.get('contextValues')[1])
        if event_info.startswith("Added"):
            event_info = event_info.replace('{storage_pool_name}', element.get('contextValues')[3])
        return user_info, event_info

    @staticmethod
    def NFSDatastoreAudit(element):
        user_info = element.get('contextValues')[-1]
        if element.get('contextValues')[-2].startswith("Creation"):
            event_info = element.get('contextValues')[-2].replace('{datastore_name}',
                                                                  element.get('contextValues')[0])
            event_info = event_info.replace('{container_name}', element.get('contextValues')[1])
        else:
            event_info = "datastore update event"
        return user_info, event_info

    @staticmethod
    def ReplicationSystemStateAudit(element):
        user_info = "< System Generated >"
        event_info = element.get('contextValues')[-1].replace('{snapshot_id}', element.get(
            'contextValues')[2])
        event_info = event_info.replace('{protection_domain_name}', element.get(
            'contextValues')[0])
        event_info = event_info.replace('{remote_name}', element.get(
            'contextValues')[1])
        event_info = event_info.replace('{start_time}', element.get(
            'contextValues')[3])
        return user_info, event_info

    @staticmethod
    def SnapshotReadyAudit(element):
        user_info = "< System Generated >"
        event_info = element.get('contextValues')[-1].replace('{snapshot_id}', element.get(
            'contextValues')[1])
        event_info = event_info.replace('{protection_domain_name}', element.get(
            'contextValues')[0])
        return user_info, event_info

    @staticmethod
    def RemoteSiteAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[1].replace('{remote_name}',
                                                             element.get('contextValues')[0])
        return user_info, event_info

    @staticmethod
    def ProtectionDomainAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[2].replace('{protection_domain_name}',
                                                             element.get('contextValues')[0])
        return user_info, event_info

    @staticmethod
    def ProtectionDomainEntitiesAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[1].replace('{protection_domain_name}',
                                                             element.get('contextValues')[0])
        return user_info, event_info

    @staticmethod
    def RegisterVmAudit(element):
        user_info = "< System Generated >"
        event_info = element.get('contextValues')[1].replace('{vm_name}',
                                                             element.get('contextValues')[0])
        return user_info, event_info

    @staticmethod
    def RestoreProtectionDomainVMsAudit(element):
        user_info = element.get('contextValues')[-1]
        return user_info, "restore_protect_domain_vms_event"

    @staticmethod
    def ModifyProtectionDomainSnapshotAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[-2]
        return user_info, event_info

    @staticmethod
    def ProtectionDomainChangeModeAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[-2].replace('{protection_domain_name}', element.get(
            'contextValues')[0])
        event_info = event_info.replace('{desired_mode}', element.get(
            'contextValues')[2])
        return user_info, event_info

    @staticmethod
    def PdCronScheduleAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[2].replace('{cron_schedule_id_list}', element.get('contextValues')[1])
        event_info = event_info.replace('{protection_domain_name}', element.get('contextValues')[0])
        return user_info, event_info

    @staticmethod
    def UpgradeInfoAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[1].replace('{protection_domain_name}',
                                                             element.get('contextValues')[0])
        return user_info, event_info

    @staticmethod
    def SoftwareReleaseAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[2].replace('{software_type}', element.get('contextValues')[1])
        event_info = event_info.replace('{software_name}', element.get('contextValues')[0])
        return user_info, event_info

    @staticmethod
    def NFSWhiteListAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    @staticmethod
    def PdOOBScheduleAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    @staticmethod
    def DiskAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[1].replace('{disk_uuid}', element.get('contextValues')[0])
        return user_info, event_info

    @staticmethod
    def pulse_event(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    @staticmethod
    def RemoteSupportAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    @staticmethod
    def SnmpInfoAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    @staticmethod
    def ClusterParamsAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    @staticmethod
    def HealthCheckPluginAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    @staticmethod
    def FileServerAudit(element):
        user_info = "< System Generated >"
        event_info = element.get('contextValues')[-1].replace('{file_server_name}', element.get('contextValues')[1])
        return user_info, event_info

    @staticmethod
    def PasswordAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[1].replace('{username}', element.get('contextValues')[0])
        return user_info, event_info

    @staticmethod
    def DirectoryRoleMappingAudit(element):
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[-2].replace('{role_name}', element.get('contextValues')[1])
        event_info = event_info.replace('{entity_type}', element.get('contextValues')[2])
        event_info = event_info.replace('{directory_name}', element.get('contextValues')[0])
        return user_info, event_info

