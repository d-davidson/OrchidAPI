import pytest

def check_status_code(response, expected_code=200):
    assert response.status_code == expected_code

def test_trivial_getters(basic_auth_api):
    # time
    check_status_code(basic_auth_api.get_server_time())
    check_status_code(basic_auth_api.get_server_time(extended=False))
    # discoverable
    check_status_code(basic_auth_api.get_discovered_cameras())
    check_status_code(basic_auth_api.get_orchids())
    check_status_code(basic_auth_api.get_orchid())
    # cameras
    check_status_code(basic_auth_api.get_cameras())
    check_status_code(basic_auth_api.get_cameras_disk_usage())
    check_status_code(basic_auth_api.get_tz_list())
    # streams
    check_status_code(basic_auth_api.get_streams())
    check_status_code(basic_auth_api.get_stream_statuses())
    # archives
    check_status_code(basic_auth_api.get_archives())
    check_status_code(basic_auth_api.get_archives_per_day())
    # frame puller
    check_status_code(basic_auth_api.get_lbm_streams())
    # events
    check_status_code(basic_auth_api.get_server_events(start=0, count=10))
    check_status_code(basic_auth_api.get_stream_events(start=0, count=10))
    # logs
    check_status_code(basic_auth_api.get_server_logs(log_format='text'))
    # users
    check_status_code(basic_auth_api.get_users())
    # servers
    check_status_code(basic_auth_api.get_servers())
    check_status_code(basic_auth_api.get_server())
    check_status_code(basic_auth_api.get_server_disk_utilization())
    check_status_code(basic_auth_api.get_server_database_faults(0))
    # server properties
    check_status_code(basic_auth_api.get_server_properties_info())
    check_status_code(basic_auth_api.get_server_properties())
    check_status_code(basic_auth_api.check_properties_confirmation())
    # storages
    check_status_code(basic_auth_api.get_storages())
    check_status_code(basic_auth_api.get_storage())
    # license
    check_status_code(basic_auth_api.get_license_session())
    # endpoitns
    check_status_code(basic_auth_api.get_endpoints())
    # version
    check_status_code(basic_auth_api.get_version())
