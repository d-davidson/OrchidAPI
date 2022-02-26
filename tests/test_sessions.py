import pytest

def test_jwt_auth(jwt_api):
    assert jwt_api.get_server_properties().status_code == 200
    assert jwt_api.delete_trusted_issuer().status_code == 200
    assert jwt_api.get_server_properties().status_code == 401

def test_remote_auth(jwt_api, remote_api):
    assert remote_api.get_server_properties().status_code == 200
    assert remote_api.delete_current_session().status_code == 200
    assert remote_api.get_server_properties().status_code == 401
    assert jwt_api.delete_trusted_issuer().status_code == 200

def test_user_auth(jwt_api, user_api):
    assert user_api.get_cameras().status_code == 200
    assert user_api.delete_current_session().status_code == 200
    assert user_api.get_cameras().status_code == 401
    assert jwt_api.delete_trusted_issuer().status_code == 200

def test_session_mgmt(jwt_api, user_api, remote_api):
    user_session_id = user_api.get_session_info().body['id']
    assert user_api.get_sessions().status_code == 200
    assert user_api.get_session(user_session_id).status_code == 200
    assert jwt_api.delete_sessions(session_type='user')
    assert user_api.delete_session(user_session_id).status_code == 401
    remote_session_id = remote_api.get_session_info().body['id']
    assert remote_api.get_session_identity().status_code == 200
    assert remote_api.delete_session(remote_session_id).status_code == 200
    assert remote_api.get_session_identity().status_code == 401
    assert jwt_api.delete_trusted_issuer().status_code == 200
