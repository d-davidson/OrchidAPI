import time
import jwt
import secrets
import pytest

from orchid_api import OrchidAPI, BearerAuth
from config import server_config

SERVER_URI = server_config['uri']
USER = server_config['user']
PASSWORD = server_config['password']

@pytest.fixture
def secret():
    return secrets.token_bytes(32)

@pytest.fixture
def encoded_jwt(secret):
    iat = int(time.time())
    exp = iat + 300
    encoded_jwt = jwt.encode({'iat': iat, 'exp': exp}, secret, algorithm='HS256'
                            ).decode('utf-8')
    return encoded_jwt

@pytest.fixture
def basic_auth_api():
    return OrchidAPI(SERVER_URI, auth=(USER, PASSWORD))

@pytest.fixture
def jwt_api(secret, basic_auth_api, encoded_jwt):
    assert basic_auth_api.get_trusted_issuer().status_code == 404
    assert basic_auth_api.create_trusted_issuer(basic_auth_api.get_orchid().body['uuid'], secret,
                                                description='testing').status_code == 201
    return OrchidAPI(SERVER_URI, auth=BearerAuth(encoded_jwt))

@pytest.fixture
def remote_api(jwt_api):
    scope = {
        'baseScope': ['config'],
        'cameraScope': []
        }
    token = jwt_api.create_remote_session('RemoteTest', scope=scope).body['id']
    return OrchidAPI(SERVER_URI, auth=BearerAuth(token))

@pytest.fixture
def user_api():
    user_api = OrchidAPI(SERVER_URI)
    session_token = user_api.create_user_session(USER, PASSWORD).body['id']
    user_api.set_bearer_token(session_token)
    return user_api
