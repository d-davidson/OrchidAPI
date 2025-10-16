"""OrchidAPI: Orchid Core VMS API wrapper.
Orchid API documentation: https://orchid.ipconfigure.com/api/.
"""

import json
import requests

from typing import Union, Tuple

__version__ = '1.0.0'

class BearerAuth(requests.auth.AuthBase):
    """Bearer authorization handler for requests library."""

    def __init__(self, token: str) -> None:
        """BearerAuth constructor.

        Parameters:
        token: Bearer authentication token.
        """
        self.token = token

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        request.headers['Authorization'] = f'Bearer {self.token}'
        return request

class OrchidAPI:
    """Orchid Core VMS API wrapper implementation."""

    def __init__(self, address: str, auth: Union[BearerAuth, Tuple[str, str]]=None, user: str=None,
                 password: str=None, timeout: Union[float, Tuple[float, float]]=(30.0, 30.0)) -> None:
        """OrchidAPI constructor.

        Parameters:
        address: Address of the Orchid Core VMS server.

        auth: Orchid Core VMS Authentication. Can be of form `('user', 'password')` for basic
        authentication, or `BearerAuth(token)` for bearer authentication. If `user` and
        `password` are supplied, this parameter is ignored.

        user: An Orchid Core VMS user.

        password: The password to `user`.

        timeout: Timeout (in seconds) for server connections and/or reads. If single value
        is supplied the value sets both connection and read timeout. To set the values
        separately, specify a tuple of the form: (connection, read).
        """
        self.server_address = address
        self.session = requests.Session()
        self.session.auth = (user, password) if user and password else auth
        self.timeout = timeout if isinstance(timeout, tuple) else (timeout, timeout)

    def set_bearer_token(self, token: str) -> None:
        """Set the bearer authorization token for HTTP requests.

        Parameters:
        token: Bearer authorization token to set.
        """
        self.session.auth = BearerAuth(token)

    def request(self, method: str, path: str, data: Union[dict, bytes]=None) -> requests.Response:
        """Make an HTTP request to the Orchid server.
        
        Parameters:
        method: The HTTP method (e.g. GET, POST, etc).

        path: The endpoint path (e.g. /cameras/1).

        data: Data, if any. Can be `None`, `dict`, or `bytes`.
        """
        if isinstance(data, dict):
            data = json.dumps(data)
        return self.session.request(method, f'{self.server_address}/service/{path.lstrip("/")}',
                                    data=data, timeout=self.timeout)

    def get(self, path: str) -> requests.Response:
        return self.request('GET', path)

    def put(self, path: str, body: Union[dict, bytes]=None) -> requests.Response:
        return self.request('PUT', path, data=body)

    def post(self, path: str, body: Union[dict, bytes]=None) -> requests.Response:
        return self.request('POST', path, data=body)

    def patch(self, path: str, body: dict=None) -> requests.Response:
        return self.request('PATCH', path, data=body)

    def delete(self, path: str) -> requests.Response:
        return self.request('DELETE', path)
