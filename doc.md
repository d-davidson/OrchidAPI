<a id="__init__"></a>

# \_\_init\_\_

OrchidAPI: Orchid Core VMS API wrapper.
Orchid API documentation: https://orchid.ipconfigure.com/api/.

<a id="__init__.BearerAuth"></a>

## BearerAuth Objects

```python
class BearerAuth(requests.auth.AuthBase)
```

Bearer authorization handler for requests library.

<a id="__init__.BearerAuth.__init__"></a>

#### \_\_init\_\_

```python
def __init__(token: str) -> None
```

BearerAuth constructor.

**Arguments**:

- `token` - Bearer authentication token.

<a id="__init__.OrchidAPI"></a>

## OrchidAPI Objects

```python
class OrchidAPI()
```

Orchid Core VMS API wrapper implementation.

<a id="__init__.OrchidAPI.__init__"></a>

#### \_\_init\_\_

```python
def __init__(
    address: str,
    auth: Union[BearerAuth, Tuple[str, str]] = None,
    user: str = None,
    password: str = None,
    timeout: Union[float, Tuple[float, float]] = (30.0, 30.0)
) -> None
```

OrchidAPI constructor.

**Arguments**:

- `address` - Address of the Orchid Core VMS server.
  
- `auth` - Orchid Core VMS Authentication. Can be of form `('user', 'password')` for basic
  authentication, or `BearerAuth(token)` for bearer authentication. If `user` and
  `password` are supplied, this parameter is ignored.
  
- `user` - An Orchid Core VMS user.
  
- `password` - The password to `user`.
  
- `timeout` - Timeout (in seconds) for server connections and/or reads. If single value
  is supplied the value sets both connection and read timeout. To set the values
  separately, specify a tuple of the form: (connection, read).

<a id="__init__.OrchidAPI.set_bearer_token"></a>

#### set\_bearer\_token

```python
def set_bearer_token(token: str) -> None
```

Set the bearer authorization token for HTTP requests.

**Arguments**:

- `token` - Bearer authorization token to set.

<a id="__init__.OrchidAPI.request"></a>

#### request

```python
def request(method: str,
            path: str,
            data: Union[dict, bytes] = None) -> requests.Response
```

Make an HTTP request to the Orchid server.

**Arguments**:

- `method` - The HTTP method (e.g. GET, POST, etc).
  
- `path` - The endpoint path (e.g. /cameras/1).
  
- `data` - Data, if any. Can be `None`, `dict`, or `bytes`.

<a id="__init__.OrchidAPI.get"></a>

#### get

```python
def get(path: str) -> requests.Response
```

Make an HTTP GET request to the Orchid server.

<a id="__init__.OrchidAPI.put"></a>

#### put

```python
def put(path: str, body: Union[dict, bytes] = None) -> requests.Response
```

Make an HTTP PUT request to the Orchid server.

<a id="__init__.OrchidAPI.post"></a>

#### post

```python
def post(path: str, body: Union[dict, bytes] = None) -> requests.Response
```

Make an HTTP POST request to the Orchid server.

<a id="__init__.OrchidAPI.patch"></a>

#### patch

```python
def patch(path: str, body: dict = None) -> requests.Response
```

Make an HTTP PATCH request to the Orchid server.

<a id="__init__.OrchidAPI.delete"></a>

#### delete

```python
def delete(path: str) -> requests.Response
```

Make an HTTP DELETE request to the Orchid server.

