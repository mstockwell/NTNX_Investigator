from flask import session
import requests
import datetime
import time
import json
from json2html import *

REST_URL_SUFFIX = 'https://%s:9440/PrismGateway/services/rest/v1'
my_session = requests.Session()


def test_credentials(username, password, ip_address):
    session['ip_address'] = ip_address
    base_url = REST_URL_SUFFIX%session['ip_address']
    my_session.auth = (username, password)
    my_session.verify = False
    my_session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
    serverResponse = my_session.get(base_url + "/cluster", timeout=20)
    return serverResponse.status_code, json.loads(serverResponse.text)

def get_events_data(investigate_date):
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

    def rep_sys_state_event():
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

    def snap_ready_event():
        user_info = "< System Generated >"
        event_info = element.get('contextValues')[-1].replace('{snapshot_id}', element.get(
            'contextValues')[1])
        event_info = event_info.replace('{protection_domain_name}', element.get(
            'contextValues')[0])
        return user_info, event_info

    def remote_site_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[1].replace('{remote_name}',
                                                             element.get('contextValues')[0])
        return user_info, event_info

    def protection_domain_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[2].replace('{protection_domain_name}',
                                                             element.get('contextValues')[0])
        return user_info, event_info

    def protect_domain_entities_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[1].replace('{protection_domain_name}',
                                                             element.get('contextValues')[0])
        return user_info, event_info

    def register_vm_event():
        user_info = "< System Generated >"
        event_info = element.get('contextValues')[1].replace('{vm_name}',
                                                             element.get('contextValues')[0])
        return user_info, event_info

    def restore_proctect_domain_vms_event():
        user_info = element.get('contextValues')[-1]
        return user_info, "restore_protect_domain_vms_event"

    def mod_protect_domain_snap_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[-2]
        return user_info, event_info

    def protect_domain_change_mode_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[-2].replace('{protection_domain_name}', element.get(
            'contextValues')[0])
        event_info = event_info.replace('{desired_mode}', element.get(
            'contextValues')[2])
        return user_info, event_info

    def pd_cron_sched_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[2].replace('{cron_schedule_id_list}', element.get('contextValues')[1])
        event_info = event_info.replace('{protection_domain_name}', element.get('contextValues')[0])
        return user_info, event_info

    def upgrade_info_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[1].replace('{protection_domain_name}', element.get('contextValues')[0])
        return user_info, event_info

    def software_release_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[2].replace('{software_type}', element.get('contextValues')[1])
        event_info = event_info.replace('{software_name}', element.get('contextValues')[0])
        return user_info, event_info

    def nfs_whitelist_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    def pd_OOB_sched_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    def disk_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[1].replace('{disk_uuid}', element.get('contextValues')[0])
        return user_info, event_info

    def pulse_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    def remote_support_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    def snmp_info_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info


    def cluster_params_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    def health_check_plugin_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[0]
        return user_info, event_info

    def file_server_event():
        user_info = "< System Generated >"
        event_info = element.get('contextValues')[-1].replace('{file_server_name}', element.get('contextValues')[1])
        return user_info, event_info

    def password_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[1].replace('{username}', element.get('contextValues')[0])
        return user_info, event_info

    def directory_role_mapping_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[-2].replace('{role_name}', element.get('contextValues')[1])
        event_info = event_info.replace('{entity_type}', element.get('contextValues')[2])
        event_info = event_info.replace('{directory_name}', element.get('contextValues')[0])
        return user_info, event_info

    event_types = {
        'LoginInfoAudit': login_event,
        'ContainerAudit': container_event,
        'NFSDatastoreAudit': nfs_datastore_event,
        'DiskAudit': disk_event,
        'ReplicationSystemStateAudit': rep_sys_state_event,
        'SnapshotReadyAudit': snap_ready_event,
        'RemoteSiteAudit': remote_site_event,
        'RegisterVmAudit': register_vm_event,
        'RestoreProtectionDomainVMsAudit': restore_proctect_domain_vms_event,
        'ProtectionDomainAudit': protection_domain_event,
        'ProtectionDomainChangeModeAudit': protect_domain_change_mode_event,
        'ProtectionDomainEntitiesAudit': protect_domain_entities_event,
        'ModifyProtectionDomainSnapshotAudit': mod_protect_domain_snap_event,
        'PdCronScheduleAudit': pd_cron_sched_event,
        'UpgradeInfoAudit': upgrade_info_event,
        'SoftwareReleaseAudit': software_release_event,
        'NFSWhiteListAudit': nfs_whitelist_event,
        'PdOOBScheduleAudit': pd_OOB_sched_event,
        'PulseAudit': pulse_event,
        'RemoteSupportAudit' : remote_support_event,
        'SnmpInfoAudit': snmp_info_event,
        'ClusterParamsAudit': cluster_params_event,
        'HealthCheckPluginAudit': health_check_plugin_event,
        'FileServerAudit': file_server_event,
        'PasswordAudit': password_event,
        'DirectoryRoleMappingAudit': directory_role_mapping_event,
    }

    eventsURL = create_event_rest_url(investigate_date)
    serverResponse = my_session.get(eventsURL)
    json_events = json.loads(serverResponse.text)
    print json2html.convert(json=json_events)
    event_list = []
    for element in json_events['entities']:
        event_time = time.gmtime(element.get('createdTimeStampInUsecs')/1000000)
        event_user, event_msg = event_types[element.get('alertTypeUuid')]()
        event_list.append((event_user, event_msg,time.strftime('%H:%M:%S', event_time)))
    event_list.sort(key=lambda tup: tup[2])
    return event_list


from NTNXWhoDidWhat import app

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as ex:
        print ex
        sys.exit(1)
