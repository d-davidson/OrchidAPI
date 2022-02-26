import pytest

def test_byte_response(basic_auth_api):
    assert isinstance(basic_auth_api.get_server_logs(log_format='gzip').body, bytes)

def test_str_response(basic_auth_api):
    assert isinstance(basic_auth_api.get_server_time(extended=False).body, str)

def test_dict_response(basic_auth_api):
    assert isinstance(basic_auth_api.get_server_time(extended=True).body, dict)
