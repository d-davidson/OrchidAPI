<a id="orchid_api"></a>

# orchid\_api

OrchidAPI: Orchid Core VMS API wrapper.

This library is implemented in accordance with the Orchid Core VMS
API documentation: https://orchid.ipconfigure.com/api/.

<a id="orchid_api.BearerAuth"></a>

## BearerAuth Objects

```python
class BearerAuth(requests.auth.AuthBase)
```

Bearer authorization handler for requests library.

<a id="orchid_api.BearerAuth.__init__"></a>

#### \_\_init\_\_

```python
def __init__(token: str) -> None
```

BearerAuth constructor.

**Arguments**:

- `token` - Bearer authentication token.

<a id="orchid_api.OrchidAPI"></a>

## OrchidAPI Objects

```python
class OrchidAPI()
```

Orchid Core VMS API wrapper implementation.

<a id="orchid_api.OrchidAPI.__init__"></a>

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
  separately, specify a tuple of the form: (<connection>, <read>).

<a id="orchid_api.OrchidAPI.set_bearer_token"></a>

#### set\_bearer\_token

```python
def set_bearer_token(token: str) -> None
```

Set the bearer authorization token for HTTP requests.

**Arguments**:

- `token` - Bearer authorization token to set.

<a id="orchid_api.OrchidAPI.get_server_time"></a>

#### get\_server\_time

```python
def get_server_time(extended: bool = True) -> requests.Response
```

Get the Orchid Core VMS server time (in epoch milliseconds, UTC).

**Arguments**:

- `extended` - If true, return extended response that includes timezone
  information. Otherwise, return epoch timestamp only.

<a id="orchid_api.OrchidAPI.get_trusted_issuer"></a>

#### get\_trusted\_issuer

```python
def get_trusted_issuer() -> requests.Response
```

Retrieve the current trusted issuer.

<a id="orchid_api.OrchidAPI.create_trusted_issuer"></a>

#### create\_trusted\_issuer

```python
def create_trusted_issuer(orchid_uuid: str,
                          secret: bytes,
                          description: str = '',
                          uri: str = '') -> requests.Response
```

Create a trusted issuer.

**Arguments**:

- `orchid_uuid` - UUID for the Orchid Core VMS server.
  
- `secret` - 32-byte shared secret used to create JWT.
  
- `description` - Describes the trusted issue.
  
- `uri` - URI to the trusted issuer.

<a id="orchid_api.OrchidAPI.delete_trusted_issuer"></a>

#### delete\_trusted\_issuer

```python
def delete_trusted_issuer() -> requests.Response
```

Delete the trusted issuer.

<a id="orchid_api.OrchidAPI.get_session_identity"></a>

#### get\_session\_identity

```python
def get_session_identity() -> requests.Response
```

Get the identity of current session.

<a id="orchid_api.OrchidAPI.get_session_info"></a>

#### get\_session\_info

```python
def get_session_info() -> requests.Response
```

Get the current session information.

<a id="orchid_api.OrchidAPI.delete_current_session"></a>

#### delete\_current\_session

```python
def delete_current_session() -> requests.Response
```

Delete the current session.

<a id="orchid_api.OrchidAPI.create_user_session"></a>

#### create\_user\_session

```python
def create_user_session(username: str,
                        password: str,
                        expires_in: int = 3600,
                        cookie: str = 'session') -> requests.Response
```

Create a new user session.

**Arguments**:

- `username` - Orchid Core VMS username.
  
- `password` - Password for username.
  
- `expires_in` - Expiration for user session (in seconds).
  
- `cookie` - Type of session cookie: [persistent, session].

<a id="orchid_api.OrchidAPI.create_remote_session"></a>

#### create\_remote\_session

```python
def create_remote_session(session_name: str,
                          expires_in: int = 3600,
                          cookie: str = 'session',
                          scope: dict = None) -> requests.Response
```

Create a new remote session.

**Arguments**:

- `session_name` - Name of the remote session.
  
- `expires_in` - Expiration for remote session (in seconds).
  
- `cookie` - Type of session cookie: [persistent, session].
  
- `scope` - Permission sets.

<a id="orchid_api.OrchidAPI.get_sessions"></a>

#### get\_sessions

```python
def get_sessions(session_type: str = None) -> requests.Response
```

Get all sessions associated to Orchid Core VMS server.

**Arguments**:

- `session_type` - Session type filter: [user, remote].
  If not set, all session types are retrieved.

<a id="orchid_api.OrchidAPI.delete_sessions"></a>

#### delete\_sessions

```python
def delete_sessions(session_type: str = None) -> requests.Response
```

Delete all sessions.

**Arguments**:

- `session_type` - Session type filter: [user, remote].
  If not set, all session types are deleted.

<a id="orchid_api.OrchidAPI.get_session"></a>

#### get\_session

```python
def get_session(session_id: str) -> requests.Response
```

Get a session by ID.

**Arguments**:

- `session_id` - ID of the session to retrieve.

<a id="orchid_api.OrchidAPI.delete_session"></a>

#### delete\_session

```python
def delete_session(session_id: str) -> requests.Response
```

Delete a session by ID.

**Arguments**:

- `session_id` - ID of the session to delete.

<a id="orchid_api.OrchidAPI.get_discovered_cameras"></a>

#### get\_discovered\_cameras

```python
def get_discovered_cameras() -> requests.Response
```

Get all of the camera discovered via ONVIF autodiscovery.

<a id="orchid_api.OrchidAPI.get_orchids"></a>

#### get\_orchids

```python
def get_orchids() -> requests.Response
```

Get all the discovered Orchid Core VMS servers.

<a id="orchid_api.OrchidAPI.get_orchid"></a>

#### get\_orchid

```python
def get_orchid(orchid_id: int = 1) -> requests.Response
```

Get a discovered Orchid Core VMS

**Arguments**:

- `orchid_id` - ID of the Orchid Core VMS.

<a id="orchid_api.OrchidAPI.get_cameras"></a>

#### get\_cameras

```python
def get_cameras() -> requests.Response
```

Get all registered cameras.

<a id="orchid_api.OrchidAPI.register_onvif_camera"></a>

#### register\_onvif\_camera

```python
def register_onvif_camera(address: str,
                          camera_user: str,
                          password: str,
                          name: str = None,
                          https: bool = False) -> requests.Response
```

Register an ONVIF compatible camera.

**Arguments**:

- `address` - IP address of the camera (e.g. 192.168.202.55).
  
- `camera_user` - A valid username registered on the camera.
  
- `password` - Password for camera user.
  
- `name` - Name of the camera (defaults to `address`).
  
- `https` - If true, use https scheme for registration. Otherwise use http.

<a id="orchid_api.OrchidAPI.register_rtsp_camera"></a>

#### register\_rtsp\_camera

```python
def register_rtsp_camera(uri: str,
                         camera_user: str,
                         password: str,
                         name: str = None) -> requests.Response
```

Register a generic RTSP camera.

**Arguments**:

- `uri` - URI to the RTSP stream.
  
- `camera_user` - A valid username registered on the camera.
  
- `password` - Password for camera user.
  
- `name` - Name of the camera (defaults to `uri`).

<a id="orchid_api.OrchidAPI.get_camera"></a>

#### get\_camera

```python
def get_camera(camera_id: int) -> requests.Response
```

Get a camera by ID.

**Arguments**:

- `camera_id` - ID of camera to retrieve.

<a id="orchid_api.OrchidAPI.patch_camera"></a>

#### patch\_camera

```python
def patch_camera(camera_id: int, body: dict) -> requests.Response
```

Patch a camera (partial update).

**Arguments**:

- `camera_id` - ID of camera to update.
  
- `body` - Camera resource PATCH body.

<a id="orchid_api.OrchidAPI.delete_camera"></a>

#### delete\_camera

```python
def delete_camera(camera_id: int) -> requests.Response
```

Delete a camera.

**Arguments**:

- `camera_id` - ID of camera to delete.

<a id="orchid_api.OrchidAPI.verify_camera"></a>

#### verify\_camera

```python
def verify_camera(camera_id: int) -> requests.Response
```

Verify a camera is pingable.

**Arguments**:

- `camera_id` - ID of camera to ping.

<a id="orchid_api.OrchidAPI.get_cameras_disk_usage"></a>

#### get\_cameras\_disk\_usage

```python
def get_cameras_disk_usage() -> requests.Response
```

Get the archive disk usage of all cameras.

<a id="orchid_api.OrchidAPI.get_tz_list"></a>

#### get\_tz\_list

```python
def get_tz_list()
```

Get a list if IANA to POSIX timezone mappings.

<a id="orchid_api.OrchidAPI.get_camera_ptz_position"></a>

#### get\_camera\_ptz\_position

```python
def get_camera_ptz_position(camera_id: int) -> requests.Response
```

Get a camera's current PTZ position.

**Arguments**:

- `camera_id` - ID of camera to retrieve PTZ position for.

<a id="orchid_api.OrchidAPI.set_camera_ptz_position"></a>

#### set\_camera\_ptz\_position

```python
def set_camera_ptz_position(camera_id: int, body: dict) -> requests.Response
```

Set a camera's PTZ position.

**Arguments**:

- `camera_id` - ID of camera to set PTZ position for.
  
- `body` - Camera PTZ resource body.

<a id="orchid_api.OrchidAPI.get_camera_ptz_presets"></a>

#### get\_camera\_ptz\_presets

```python
def get_camera_ptz_presets(camera_id: int) -> requests.Response
```

Get a list of a camera's PTZ presets.

**Arguments**:

- `camera_id` - ID of camera to retrieve PTZ preset list for.

<a id="orchid_api.OrchidAPI.set_camera_ptz_preset"></a>

#### set\_camera\_ptz\_preset

```python
def set_camera_ptz_preset(camera_id: int,
                          preset_name: str) -> requests.Response
```

Set a camera's PTZ preset at the camera's current PTZ position.

**Arguments**:

- `camera_id` - ID of camera to set PTZ preset for.
  
- `preset_name` - Name of preset.

<a id="orchid_api.OrchidAPI.delete_camera_ptz_preset"></a>

#### delete\_camera\_ptz\_preset

```python
def delete_camera_ptz_preset(camera_id: int,
                             preset_token: str) -> requests.Response
```

Delete the PTZ preset on a camera.

**Arguments**:

- `camera_id` - ID of camera to delete PTZ preset for.
  
- `preset_token` - Token/ID of the PTZ preset to delete.

<a id="orchid_api.OrchidAPI.get_camera_streams"></a>

#### get\_camera\_streams

```python
def get_camera_streams(camera_id: int) -> requests.Response
```

List all the stream's for a camera.

**Arguments**:

- `camera_id` - ID of camera to retrieve streams for.

<a id="orchid_api.OrchidAPI.register_stream"></a>

#### register\_stream

```python
def register_stream(camera_id: int, body: dict) -> requests.Response
```

Register a new stream for a camera.

**Arguments**:

- `camera_id` - ID of camera to register a new stream for.
  
- `body` - Stream resource body.

<a id="orchid_api.OrchidAPI.get_camera_stream"></a>

#### get\_camera\_stream

```python
def get_camera_stream(camera_id: int, stream_id: int) -> requests.Response
```

Get a camera's stream.

**Arguments**:

- `camera_id` - ID of camera that stream is associated to.
  
- `stream_id` - ID of stream to retrieve.

<a id="orchid_api.OrchidAPI.patch_stream"></a>

#### patch\_stream

```python
def patch_stream(camera_id: int, stream_id: int,
                 body: dict) -> requests.Response
```

Patch a camera's stream (partial update).

**Arguments**:

- `camera_id` - ID of camera that stream is associated to.
  
- `stream_id` - ID of stream to update.
  
- `body` - Stream resource PATCH body.

<a id="orchid_api.OrchidAPI.update_stream"></a>

#### update\_stream

```python
def update_stream(camera_id: int, stream_id: int,
                  body: dict) -> requests.Response
```

Update a camera's stream (full update).

**Arguments**:

- `camera_id` - ID of camera that stream is associated to.
  
- `stream_id` - ID of stream to update.
  
- `body` - Stream resource body.

<a id="orchid_api.OrchidAPI.delete_stream"></a>

#### delete\_stream

```python
def delete_stream(camera_id: int, stream_id: int) -> requests.Response
```

Delete a camera's stream.

**Arguments**:

- `camera_id` - ID of camera that stream is associated to.
  
- `stream_id` - ID of stream to delete.

<a id="orchid_api.OrchidAPI.restart_stream"></a>

#### restart\_stream

```python
def restart_stream(camera_id: int, stream_id: int) -> requests.Response
```

Restart a camera stream.

**Arguments**:

- `camera_id` - ID of camera that stream is associated to.
  
- `stream_id` - ID of stream to restart.

<a id="orchid_api.OrchidAPI.get_stream_motion_mask"></a>

#### get\_stream\_motion\_mask

```python
def get_stream_motion_mask(camera_id: int,
                           stream_id: int) -> requests.Response
```

Get a camera stream's motion mask.

**Arguments**:

- `camera_id` - ID of camera that stream is associated to.
  
- `stream_id` - ID of stream to get motion mask for

<a id="orchid_api.OrchidAPI.upload_stream_motion_mask"></a>

#### upload\_stream\_motion\_mask

```python
def upload_stream_motion_mask(camera_id: int, stream_id: int,
                              mask: bytes) -> requests.Response
```

Upload a camera stream's motion mask.

**Arguments**:

- `camera_id` - ID of camera that stream is associated to.
  
- `stream_id` - ID of stream to upload motion mask for.
  
- `mask` - PNG image of stream frame, in bytes, containing motion mask.

<a id="orchid_api.OrchidAPI.delete_stream_motion_mask"></a>

#### delete\_stream\_motion\_mask

```python
def delete_stream_motion_mask(camera_id: int,
                              stream_id: int) -> requests.Response
```

Delete a camera stream's motion mask.

**Arguments**:

- `camera_id` - ID of camera that stream is associated to.
  
- `stream_id` - ID of stream to delete motion mask for.

<a id="orchid_api.OrchidAPI.get_streams"></a>

#### get\_streams

```python
def get_streams() -> requests.Response
```

List all registered streams.

<a id="orchid_api.OrchidAPI.get_stream_statuses"></a>

#### get\_stream\_statuses

```python
def get_stream_statuses()
```

List the status of all registered streams.

<a id="orchid_api.OrchidAPI.get_stream"></a>

#### get\_stream

```python
def get_stream(stream_id: int) -> requests.Response
```

Get a stream.

**Arguments**:

- `stream_id` - ID of stream to retrieve.

<a id="orchid_api.OrchidAPI.get_stream_frame"></a>

#### get\_stream\_frame

```python
def get_stream_frame(stream_id: int,
                     time: int = 0,
                     height: int = 0,
                     width: int = 0,
                     fallback: bool = False) -> requests.Response
```

Get a stream JPEG frame.

**Arguments**:

- `stream_id` - ID of stream to retrieve frame for.
  
- `time` - Frame time (server time in epoch milliseconds, UTC). 0 is a special value for
  retrieving first frame from the latest archive.
  
- `height` - Desired frame height. 0 is a special value for using the streams native resolution.
  
- `width` - Desired frame width. 0 is a special value for using the streams native resolution.
  
- `fallback` - If true, on errors, a black GIF wil be returned. Otherwise on errors, an error code
  is returned.

<a id="orchid_api.OrchidAPI.export_stream"></a>

#### export\_stream

```python
def export_stream(stream_id: int,
                  start: int,
                  stop: int,
                  container: str = 'mkv') -> requests.Response
```

Export media from a stream.

**Arguments**:

- `stream_id` - ID of stream to export media for.
  
- `start` - Start time (server time in epoch milliseconds, UTC).
  
- `stop` - Stop time (server time in epoch milliseconds, UTC).
  
- `container` - Video export format: [mkv, mov, mp4, dewarp, dewarp-parent].

<a id="orchid_api.OrchidAPI.get_stream_metadata"></a>

#### get\_stream\_metadata

```python
def get_stream_metadata(camera_id: int, stream_id: int) -> requests.Response
```

Get a camera stream's metadata.

**Arguments**:

- `camera_id` - ID of camera that stream is associated to.
  
- `stream_id` - ID of stream to retrieve metadata for.

<a id="orchid_api.OrchidAPI.get_stream_status"></a>

#### get\_stream\_status

```python
def get_stream_status(stream_id: int) -> requests.Response
```

Get status of a stream.

**Arguments**:

- `stream_id` - ID of stream to retrieve status for.

<a id="orchid_api.OrchidAPI.get_archives"></a>

#### get\_archives

```python
def get_archives(start: int = 0,
                 take: int = 100,
                 offset: int = 0,
                 stream_id: int = None) -> requests.Response
```

Get a list of existing archives.

**Arguments**:

- `start` - Start (server time in epoch milliseconds, UTC). If 0, defaults
  to current epoch time in milliseconds, UTC.
  
- `take` - Number of archives to return.
  
- `offset` - Number of archives to skip.
  
- `stream_id` - If specified, only retrieve archives associated to stream.

<a id="orchid_api.OrchidAPI.get_archive"></a>

#### get\_archive

```python
def get_archive(archive_id: int) -> requests.Response
```

Get an archive by ID.

**Arguments**:

- `archive_id` - ID of archive to retrieve.

<a id="orchid_api.OrchidAPI.download_archive"></a>

#### download\_archive

```python
def download_archive(archive_id: int) -> requests.Response
```

Download an archive by ID.

**Arguments**:

- `archive_id` - ID of archive to download.

<a id="orchid_api.OrchidAPI.get_archives_per_day"></a>

#### get\_archives\_per\_day

```python
def get_archives_per_day() -> requests.Response
```

Get a count of archives generated, per day.

<a id="orchid_api.OrchidAPI.get_lbm_streams"></a>

#### get\_lbm\_streams

```python
def get_lbm_streams() -> requests.Response
```

List all currently active low-bandwidth streams.

<a id="orchid_api.OrchidAPI.create_lbm_stream"></a>

#### create\_lbm\_stream

```python
def create_lbm_stream(
        stream_id: int,
        height: int,
        width: int,
        start: int = 0,
        sync: bool = False,
        rate: float = 1.0,
        wait_thres: int = 2000,
        transport: str = 'websocket-base64') -> requests.Response
```

Create a new low-bandwidth mode (LBM) stream.

**Arguments**:

- `stream_id` - ID of stream to create LBM session for.
  
- `height` - Desired resolution height.
  
- `width` - Desired resolution width.
  
- `start` - Start time of stream (server time, epoch milliseconds). Use
  0 to specify live.
  
- `sync` - If true, apply time offset to video to account for request latency.
  Only applies to playback streams.
  
- `rate` - Rate of playback stream.
  
- `wait_thres` - The max time allowed (milliseconds) to wait for media to start playing or
  to bridge a media gap.
  
- `transport` - Mode for transmitting frames: [http, websocket-base64].

<a id="orchid_api.OrchidAPI.get_lbm_stream"></a>

#### get\_lbm\_stream

```python
def get_lbm_stream(stream_uuid: str) -> requests.Response
```

Get a low-bandwidth mode stream by ID.

**Arguments**:

- `stream_uuid` - ID of low-bandwidth mode stream.

<a id="orchid_api.OrchidAPI.delete_lbm_stream"></a>

#### delete\_lbm\_stream

```python
def delete_lbm_stream(stream_uuid: str) -> requests.Response
```

Delete an LBM stream.

**Arguments**:

- `stream_uuid` - ID of low-bandwidth mode stream to delete.

<a id="orchid_api.OrchidAPI.get_lbm_frame"></a>

#### get\_lbm\_frame

```python
def get_lbm_frame(stream_uuid: str) -> requests.Response
```

Get a low-bandwidth mode stream JPEG frame from a session created for `http` mode.

**Arguments**:

- `stream_uuid` - ID of low-bandwidth mode stream to get frame for.

<a id="orchid_api.OrchidAPI.get_server_events"></a>

#### get\_server\_events

```python
def get_server_events(start: int,
                      stop: int = None,
                      count: int = None,
                      server_ids: str = None,
                      event_types: str = None) -> requests.Response
```

Get server events.

**Arguments**:

- `start` - Start time (server time in epoch milliseconds, UTC).
  
- `stop` - Stop time (server time in epoch milliseconds, UTC). If not specified
  default to time of latest server event available.
  
- `count` - Number of events to return. If not specified, return all events.
  
- `server_ids` - Comma separated string of server IDs. If specified, only retrieve events
  for listed servers.
  
- `event_types` - Comma separated string of event types. If specified, only retrieve the
  listed event types.

<a id="orchid_api.OrchidAPI.get_stream_events"></a>

#### get\_stream\_events

```python
def get_stream_events(start: int,
                      stop: int = None,
                      count: int = None,
                      stream_ids: int = None,
                      event_types: int = None) -> requests.Response
```

Get camera stream events.

**Arguments**:

- `start` - Start time (server time in epoch milliseconds, UTC).
  
- `stop` - Stop time (server time in epoch milliseconds, UTC). If not specified
  default to time of latest server event available.
  
- `count` - Number of events to return. If not specified, return all events.
  
- `stream_ids` - Comma separated string of stream IDs. If specified, only retrieve events
  for listed streams.
  
- `event_types` - Comma separated string of event types. If specified, only retrieve the
  listed event types.

<a id="orchid_api.OrchidAPI.get_camera_stream_event_histogram"></a>

#### get\_camera\_stream\_event\_histogram

```python
def get_camera_stream_event_histogram(
        start: int,
        stop: int,
        min_segment: int,
        stream_ids: str = None,
        event_types: str = None) -> requests.Response
```

Get camera stream event histogram.

**Arguments**:

- `start` - Start time (server time in epoch milliseconds, UTC).
  
- `stop` - Stop time (server time in epoch milliseconds, UTC).
  
- `min_segment` - Segment size of binned results.
  
- `stream_ids` - Comma separated string of stream IDs. If specified, only retrieve events
  for listed streams.
  
- `event_types` - Comma separated string of event types. If specified, only retrieve the
  listed event types.

<a id="orchid_api.OrchidAPI.get_server_logs"></a>

#### get\_server\_logs

```python
def get_server_logs(log_format: str = 'gzip',
                    start: int = None,
                    stop: int = None) -> requests.Response
```

Get server logs.

**Arguments**:

- `log_format` - Log file format: [gzip, text].
  
- `start` - Start time (server time in epoch milliseconds, UTC).
  If not specified, use start time of earliest server log file.
  
- `stop` - Stop time (server time in epoch milliseconds, UTC).
  If not specified, use stop time of the latest server log file.

<a id="orchid_api.OrchidAPI.get_users"></a>

#### get\_users

```python
def get_users()
```

Get all users.

<a id="orchid_api.OrchidAPI.create_user"></a>

#### create\_user

```python
def create_user(username: str,
                password: str,
                role: str = 'Manager') -> requests.Response
```

Create a new user.

**Arguments**:

- `username` - Name of new user.
  
- `password` - Password for new user.
  
- `role` - Permission scope: [Administrator, Manager, Live Viewer, Viewer].

<a id="orchid_api.OrchidAPI.get_user"></a>

#### get\_user

```python
def get_user(user_id: int) -> requests.Response
```

Get a user by ID.

**Arguments**:

- `user_id` - ID of user to retrieve.

<a id="orchid_api.OrchidAPI.update_user"></a>

#### update\_user

```python
def update_user(user_id: int, body: dict) -> requests.Response
```

Update a user (full update).

**Arguments**:

- `user_id` - ID of user to update.
  
- `body` - User resource body.

<a id="orchid_api.OrchidAPI.patch_user"></a>

#### patch\_user

```python
def patch_user(user_id: int, body: dict) -> requests.Response
```

Patch a user (partial update).

**Arguments**:

- `user_id` - ID of user to update.
  
- `body` - User resource body.

<a id="orchid_api.OrchidAPI.delete_user"></a>

#### delete\_user

```python
def delete_user(user_id: int) -> requests.Response
```

Delete a user.

**Arguments**:

- `user_id` - ID of user to delete.

<a id="orchid_api.OrchidAPI.get_servers"></a>

#### get\_servers

```python
def get_servers() -> requests.Response
```

List all servers.

<a id="orchid_api.OrchidAPI.get_server"></a>

#### get\_server

```python
def get_server(server_id: int = 1) -> requests.Response
```

Get a server by ID.

**Arguments**:

- `server_id` - ID of server to retrieve.

<a id="orchid_api.OrchidAPI.generate_server_report"></a>

#### generate\_server\_report

```python
def generate_server_report(start: int, stop: int) -> requests.Response
```

Generate a server report.

**Arguments**:

- `start` - Start time (server time in epoch milliseconds, UTC).
  
- `stop` - Stop time (server time in epoch milliseconds, UTC).

<a id="orchid_api.OrchidAPI.get_server_disk_utilization"></a>

#### get\_server\_disk\_utilization

```python
def get_server_disk_utilization() -> requests.Response
```

Get the server disk utilization.

<a id="orchid_api.OrchidAPI.get_server_database_faults"></a>

#### get\_server\_database\_faults

```python
def get_server_database_faults(start: int,
                               stop: int = None) -> requests.Response
```

Get the server's database errors.

**Arguments**:

- `start` - Start time (server time in epoch milliseconds, UTC).
  
- `stop` - Stop time (server in epoch milliseconds, UTC). If not specified.
  All database faults after start time will be retrieved.

<a id="orchid_api.OrchidAPI.get_server_properties_info"></a>

#### get\_server\_properties\_info

```python
def get_server_properties_info() -> requests.Response
```

Get information on configurable server properites.

<a id="orchid_api.OrchidAPI.get_server_properties"></a>

#### get\_server\_properties

```python
def get_server_properties() -> requests.Response
```

Get the properties the server is currently configured with.

<a id="orchid_api.OrchidAPI.update_server_properties"></a>

#### update\_server\_properties

```python
def update_server_properties(body: dict) -> requests.Response
```

Update the server properties file.

**Arguments**:

- `body` - Server properties resource body.

<a id="orchid_api.OrchidAPI.check_properties_confirmation"></a>

#### check\_properties\_confirmation

```python
def check_properties_confirmation() -> requests.Response
```

Check if changes made to the properties file needs confirmation.

<a id="orchid_api.OrchidAPI.confirm_properties"></a>

#### confirm\_properties

```python
def confirm_properties(confirmed: bool = True) -> requests.Response
```

Confirm changes made to the properties file.

**Arguments**:

- `confirmed` - If true, confirm the properties. Otherwise the
  server will revert to the previously configured settings.

<a id="orchid_api.OrchidAPI.get_storages"></a>

#### get\_storages

```python
def get_storages()
```

List all archive storage locations.

<a id="orchid_api.OrchidAPI.get_storage"></a>

#### get\_storage

```python
def get_storage(storage_id: int = 1) -> requests.Response
```

List an archive storage location by ID.

**Arguments**:

- `storage_id` - ID of storage location to retrieve.

<a id="orchid_api.OrchidAPI.get_license_session"></a>

#### get\_license\_session

```python
def get_license_session() -> requests.Response
```

Get the current Orchid VMS license session.

<a id="orchid_api.OrchidAPI.create_license_session"></a>

#### create\_license\_session

```python
def create_license_session(orchid_license: str) -> requests.Response
```

Create a new license session.

**Arguments**:

- `orchid_license` - New Orchid Core VMS license to upload.

<a id="orchid_api.OrchidAPI.delete_license_session"></a>

#### delete\_license\_session

```python
def delete_license_session() -> requests.Response
```

Delete the current license session.

<a id="orchid_api.OrchidAPI.get_endpoints"></a>

#### get\_endpoints

```python
def get_endpoints() -> requests.Response
```

Get all Orchid Core VMS API endpoints.

<a id="orchid_api.OrchidAPI.get_version"></a>

#### get\_version

```python
def get_version() -> requests.Response
```

Get version information for Orchid Core VMS install.

<a id="orchid_api.OrchidAPI.upload_ui_package"></a>

#### upload\_ui\_package

```python
def upload_ui_package(ui_package: bytes) -> requests.Response
```

Upload a signed user-interface (UI) update package.

**Arguments**:

- `ui_package` - ZIP package in bytes to upload. Note that this package must be
  signed by IPConfigure, Inc.

