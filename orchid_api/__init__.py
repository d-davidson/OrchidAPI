"""OrchidAPI: Orchid Core VMS API wrapper.

This library is implemented in accordance with the Orchid Core VMS
API documentation: https://orchid.ipconfigure.com/api/.
"""

import json
import base64
import requests

__version__ = '1.0.0'

class BearerAuth(requests.auth.AuthBase):
    """Bearer authorization handler for requests library."""

    def __init__(self, token):
        """BearerAuth constructor.

        Parameters:
        token: Bearer authentication token.
        """
        self.token = token

    def __call__(self, request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        return request

class OrchidAPI:
    """Orchid Core VMS API wrapper implementation."""

    def __init__(self, address, auth=None, user=None, password=None, connection_timeout=30):
        """OrchidAPI constructor.

        Parameters:
        address: Address of the Orchid Core VMS server.

        auth: Orchid Core VMS Authentication. Can be of form `('user', 'password')` for basic
        authentication, or `BearerAuth(token)` for bearer authentication. If `user` and
        `password` are supplied, this parameter is ignored.

        user: An Orchid Core VMS user.

        password: The password to `user`.

        connection_timeout: Timeout for HTTP requests.
        """
        self.server_address = address
        self.session = requests.Session()
        if user and password:
            self.session.auth = (user, password)
        else:
            self.session.auth = auth
        self.connection_timeout = connection_timeout

    def __del__(self):
        self.session.close()

    def set_bearer_token(self, token):
        """Set the bearer authorization token for HTTP requests.

        Parameters:
        token: Bearer authorization token to set.
        """
        self.session.auth = BearerAuth(token)

    ### Time Services

    def get_server_time(self, extended=True):
        """Get the Orchid Core VMS server time (in epoch milliseconds, UTC).

        Parameters:
        extended: If true, return extended response that includes timezone
        information. Otherwise, return epoch timestamp only.
        """
        if extended:
            return self._get('/time-extended')
        return self._get('/time')

    ### Trusted Issuer Services

    def get_trusted_issuer(self):
        """Retrieve the current trusted issuer."""
        return self._get('/trusted/issuer')

    def create_trusted_issuer(self, orchid_uuid, secret: bytes, description='', uri=''):
        """Create a trusted issuer.

        Parameters:
        orchid_uuid: UUID for the Orchid Core VMS server.

        secret: 32-byte shared secret used to create JWT.

        description: Describes the trusted issue.

        uri: URI to the trusted issuer.
        """
        body = {
            'id': orchid_uuid,
            'access_token': '',
            'key': {
                'kty': 'oct',
                'k': base64.urlsafe_b64encode(secret).decode('utf-8')
                },
            'description': description,
            'uri': uri
            }
        return self._post('/trusted/issuer?version=2', body)

    def delete_trusted_issuer(self):
        """Delete the trusted issuer."""
        return self._delete('/trusted/issuer')

    ### Sessions Services

    def get_session_identity(self):
        """Get the identity of current session."""
        return self._get('/identity')

    def get_session_info(self):
        """Get the current session information."""
        return self._get('/sessions/me')

    def delete_current_session(self):
        """Delete the current session."""
        return self._delete('/sessions/me')

    def create_user_session(self, username, password, expires_in=3600, cookie='session'):
        """Create a new user session.

        Parameters:
        username: Orchid Core VMS username.

        password: Password for username.

        expires_in: Expiration for user session (in seconds).

        cookie: Type of session cookie: [persistent, session].
        """
        body = {
            'username': username,
            'password': password,
            'expiresIn': expires_in,
            'cookie': cookie
            }
        return self._post('/sessions/user', body)

    def create_remote_session(self, session_name, expires_in=3600, cookie='session', scope: dict=None):
        """Create a new remote session.

        Parameters:
        session_name: Name of the remote session.

        expires_in: Expiration for remote session (in seconds).

        cookie: Type of session cookie: [persistent, session].

        scope: Permission sets.
        """
        body = {
            'name': session_name,
            'expiresIn': expires_in,
            'cookie': cookie
            }
        if scope:
            body['scope'] = scope
        return self._post('/sessions/remote', body)

    def get_sessions(self, session_type=None):
        """Get all sessions associated to Orchid Core VMS server.

        Parameters:
        session_type: Session type filter: [user, remote].
        If not set, all session types are retrieved.
        """
        if session_type:
            return self._get(f'/sessions?type={session_type}')
        return self._get('/sessions')

    def delete_sessions(self, session_type=None):
        """Delete all sessions.

        Parameters:
        session_type: Session type filter: [user, remote].
        If not set, all session types are deleted.
        """
        if session_type:
            return self._delete(f'/sessions?type={session_type}')
        return self._delete('/sessions')

    def get_session(self, session_id: str):
        """Get a session by ID.

        Parameters:
        session_id: ID of the session to retrieve.
        """
        return self._get(f'/sessions?{session_id}')

    def delete_session(self, session_id):
        """Delete a session by ID.

        Parameters:
        session_id: ID of the session to delete.
        """
        return self._delete(f'/sessions?{session_id}')

    ### Discoverable Services

    def get_discovered_cameras(self):
        """Get all of the camera discovered via ONVIF autodiscovery."""
        return self._get('/discoverable/cameras')

    def get_orchids(self):
        """Get all the discovered Orchid Core VMS servers."""
        return self._get('/discoverable/orchids')

    def get_orchid(self, orchid_id=1):
        """Get a discovered Orchid Core VMS

        Parameters:
        orchid_id: ID of the Orchid Core VMS.
        """
        return self._get(f'/discoverable/orchids/{orchid_id}')

    ### Camera Services

    def get_cameras(self):
        """Get all registered cameras."""
        return self._get('/cameras')

    def register_onvif_camera(self, address, camera_user, password, name=None, https=False):
        """Register an ONVIF compatible camera.

        Parameters:
        address: IP address of the camera (e.g. 192.168.202.55).

        camera_user: A valid username registered on the camera.

        password: Password for camera user.

        name: Name of the camera (defaults to `address`).

        https: If true, use https scheme for registration. Otherwise use http.
        """
        if not name:
            name = address
        scheme = 'http' if not https else 'https'
        body = self._generate_cam_registration_body(f'{scheme}://{address}/onvif/device_service',
                                                    camera_user, password, name=name, driver='ONVIF')
        return self._post('/cameras', body)

    def register_rtsp_camera(self, uri, camera_user, password, name=None):
        """Register a generic RTSP camera.

        Parameters:
        uri: URI to the RTSP stream.

        camera_user: A valid username registered on the camera.

        password: Password for camera user.

        name: Name of the camera (defaults to `uri`).
        """
        if not name:
            name = uri
        body = self._generate_cam_registration_body(uri, camera_user, password,
                                                    name=name, driver='Generic RTSP')
        return self._post('/cameras', body)

    def get_camera(self, camera_id):
        """Get a camera by ID.

        Parameters:
        camera_id: ID of camera to retrieve.
        """
        return self._get(f'/cameras/{camera_id}')

    def patch_camera(self, camera_id, body):
        """Patch a camera (partial update).

        Parameters:
        camera_id: ID of camera to update.

        body: Camera resource PATCH body.
        """
        return self._patch(f'/cameras/{camera_id}', body)

    def delete_camera(self, camera_id):
        """Delete a camera.

        Parameters:
        camera_id: ID of camera to delete.
        """
        return self._delete(f'/cameras/{camera_id}')

    def verify_camera(self, camera_id):
        """Verify a camera is pingable.

        Parameters:
        camera_id: ID of camera to ping.
        """
        return self._get(f'/cameras/{camera_id}/verify')

    def get_cameras_disk_usage(self):
        """Get the archive disk usage of all cameras."""
        return self._get('/cameras/disk-usage')

    def get_tz_list(self):
        """Get a list if IANA to POSIX timezone mappings."""
        return self._get('/cameras/tz-list')

    def get_camera_ptz_position(self, camera_id):
        """Get a camera's current PTZ position.

        Parameters:
        camera_id: ID of camera to retrieve PTZ position for.
        """
        return self._get(f'/cameras/{camera_id}/position')

    def set_camera_ptz_position(self, camera_id, body):
        """Set a camera's PTZ position.

        Parameters:
        camera_id: ID of camera to set PTZ position for.

        body: Camera PTZ resource body.
        """
        return self._post(f'/cameras/{camera_id}/position', body)

    def get_camera_ptz_presets(self, camera_id):
        """Get a list of a camera's PTZ presets.

        Parameters:
        camera_id: ID of camera to retrieve PTZ preset list for.
        """
        return self._get(f'/cameras/{camera_id}/position/presets')

    def set_camera_ptz_preset(self, camera_id, preset_name):
        """Set a camera's PTZ preset at the camera's current PTZ position.

        Parameters:
        camera_id: ID of camera to set PTZ preset for.

        preset_name: Name of preset.
        """
        body = { 'name': preset_name }
        return self._post(f'/cameras/{camera_id}/position/presets', body)

    def delete_camera_ptz_preset(self, camera_id, preset_token: str):
        """Delete the PTZ preset on a camera.

        Parameters:
        camera_id: ID of camera to delete PTZ preset for.

        preset_token: Token/ID of the PTZ preset to delete.
        """
        return self._delete(f'/cameras/{camera_id}/position/presets/{preset_token}')

    ### Stream Services

    def get_camera_streams(self, camera_id):
        """List all the stream's for a camera.

        Parameters:
        camera_id: ID of camera to retrieve streams for.
        """
        return self._get(f'/cameras/{camera_id}/streams')

    def register_stream(self, camera_id, body):
        """Register a new stream for a camera.

        Parameters:
        camera_id: ID of camera to register a new stream for.

        body: Stream resource body.
        """
        return self._post(f'/cameras/{camera_id}/streams', body)

    def get_camera_stream(self, camera_id, stream_id):
        """Get a camera's stream.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to retrieve.
        """
        return self._get(f'/cameras/{camera_id}/streams/{stream_id}')

    def patch_stream(self, camera_id, stream_id, body):
        """Patch a camera's stream (partial update).

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to update.

        body: Stream resource PATCH body.
        """
        return self._patch(f'/cameras/{camera_id}/streams/{stream_id}', body)

    def update_stream(self, camera_id, stream_id, body):
        """Update a camera's stream (full update).

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to update.

        body: Stream resource body.
        """
        return self._put(f'/cameras/{camera_id}/streams/{stream_id}', body)

    def delete_stream(self, camera_id, stream_id):
        """Delete a camera's stream.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to delete.
        """
        return self._delete(f'/cameras/{camera_id}/streams/{stream_id}')

    def restart_stream(self, camera_id, stream_id):
        """Restart a camera stream.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to restart.
        """
        return self._patch(f'/cameras/{camera_id}/streams/{stream_id}/restart')

    def get_stream_motion_mask(self, camera_id, stream_id):
        """Get a camera stream's motion mask.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to get motion mask for
        """
        return self._get(f'/cameras/{camera_id}/streams/{stream_id}/motion/mask')

    def upload_stream_motion_mask(self, camera_id, stream_id, mask: bytes):
        """Upload a camera stream's motion mask.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to upload motion mask for.

        mask: PNG image of stream frame, in bytes, containing motion mask.
        """
        return self._put(f'/cameras/{camera_id}/streams/{stream_id}/motion/mask', mask)

    def delete_stream_motion_mask(self, camera_id, stream_id):
        """Delete a camera stream's motion mask.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to delete motion mask for.
        """
        return self._delete(f'/cameras/{camera_id}/streams/{stream_id}/motion/mask')

    def get_streams(self):
        """List all registered streams."""
        return self._get('/streams')

    def get_stream_statuses(self):
        """List the status of all registered streams."""
        return self._get('/streams/status')

    def get_stream(self, stream_id):
        """Get a stream.

        Parameters:
        stream_id: ID of stream to retrieve.
        """
        return self._get(f'/streams/{stream_id}')

    def get_stream_frame(self, stream_id, time=0, height=0, width=0, fallback=False):
        """Get a stream JPEG frame.

        Parameters:
        stream_id: ID of stream to retrieve frame for.

        time: Frame time (server time in epoch milliseconds, UTC). 0 is a special value for
        retrieving first frame from the latest archive.

        height: Desired frame height. 0 is a special value for using the streams native resolution.

        width: Desired frame width. 0 is a special value for using the streams native resolution.

        fallback: If true, on errors, a black GIF wil be returned. Otherwise on errors, an error code
        is returned.
        """
        return self._get(f'/streams/{stream_id}/frame?time={time}&width={width}&height={height}&fallback={fallback}')

    def export_stream(self, stream_id, start, stop, container='mkv'):
        """Export media from a stream.

        Parameters:
        stream_id: ID of stream to export media for.

        start: Start time (server time in epoch milliseconds, UTC).

        stop: Stop time (server time in epoch milliseconds, UTC).

        container: Video export format: [mkv, mov, mp4, dewarp, dewarp-parent].
        """
        return self._get(f'/streams/{stream_id}/export?start={start}&stop={stop}&format={container}')

    def get_stream_metadata(self, camera_id, stream_id):
        """Get a camera stream's metadata.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to retrieve metadata for.
        """
        return self._get(f'/cameras/{camera_id}/streams/{stream_id}/metadata')

    def get_stream_status(self, stream_id):
        """Get status of a stream.

        Parameters:
        stream_id: ID of stream to retrieve status for.
        """
        return self._get(f'/streams/{stream_id}/status')

    ### Archive Services

    def get_archives(self, start=0, take=100, offset=0, stream_id=None):
        """Get a list of existing archives.

        Parameters:
        start: Start (server time in epoch milliseconds, UTC). If 0, defaults
        to current epoch time in milliseconds, UTC.

        take: Number of archives to return.

        offset: Number of archives to skip.

        stream_id: If specified, only retrieve archives associated to stream.
        """
        query_params = f'start={start}&take={take}&offset={offset}'
        if stream_id:
            query_params += f'&streamId={stream_id}'
        return self._get(f'/archives?{query_params}')

    def get_archive(self, archive_id):
        """Get an archive by ID.

        Parameters:
        archive_id: ID of archive to retrieve.
        """
        return self._get(f'/archives/{archive_id}')

    def download_archive(self, archive_id):
        """Download an archive by ID.

        Parameters:
        archive_id: ID of archive to download.
        """
        return self._get(f'/archives/{archive_id}/download')

    def get_archives_per_day(self):
        """Get a count of archives generated, per day."""
        return self._get('/archives/per-day')

    ### Frame Puller Services

    def get_lbm_streams(self):
        """List all currently active low-bandwidth streams."""
        return self._get('/low-bandwidth/streams')

    def create_lbm_stream(self, stream_id, height, width, start=0, sync=False,
                          rate=1.0, wait_thres=2000, transport='websocket-base64'):
        """Create a new low-bandwidth mode (LBM) stream.

        Parameters:
        stream_id: ID of stream to create LBM session for.

        height: Desired resolution height.

        width: Desired resolution width.

        start: Start time of stream (server time, epoch milliseconds). Use
        0 to specify live.

        sync: If true, apply time offset to video to account for request latency.
        Only applies to playback streams.

        rate: Rate of playback stream.

        wait_thres: The max time allowed (milliseconds) to wait for media to start playing or
        to bridge a media gap.

        transport: Mode for transmitting frames: [http, websocket-base64].
        """
        body = {
            'streamId': stream_id,
            'resolution': {
                'height': height,
                'width': width
                },
            'startTime': start,
            'sync': sync,
            'rate': rate,
            'waitThres': wait_thres,
            'transport': transport
            }
        return self._post('/low-bandwidth/streams', body)

    def get_lbm_stream(self, stream_uuid: str):
        """Get a low-bandwidth mode stream by ID.

        Parameters:
        stream_uuid: ID of low-bandwidth mode stream.
        """
        return self._get(f'/low-bandwidth/streams/{stream_uuid}')

    def delete_lbm_stream(self, stream_uuid: str):
        """Delete an LBM stream.

        Parameters:
        stream_uuid: ID of low-bandwidth mode stream to delete.
        """
        return self._delete(f'/low-bandwidth/streams/{stream_uuid}')

    def get_lbm_frame(self, stream_uuid: str):
        """Get a low-bandwidth mode stream JPEG frame from a session created for `http` mode.

        Parameters:
        stream_uuid: ID of low-bandwidth mode stream to get frame for.
        """
        return self._get(f'/low-bandwidth/streams/{stream_uuid}/frame')

    ### Event Services

    def get_server_events(self, start, stop=None, count=None, server_ids=None, event_types=None):
        """Get server events.

        Parameters:
        start: Start time (server time in epoch milliseconds, UTC).

        stop: Stop time (server time in epoch milliseconds, UTC). If not specified
        default to time of latest server event available.

        count: Number of events to return. If not specified, return all events.

        server_ids: Comma separated string of server IDs. If specified, only retrieve events
        for listed servers.

        event_types: Comma servers string of event types. If specified, only retrieve the
        listed event types.
        """
        query_params = self._generate_event_query_params(start, stop, count, server_ids, event_types)
        return self._get(f'/events/server?{query_params}')

    def get_stream_events(self, start, stop=None, count=None, stream_ids=None, event_types=None):
        """Get camera stream events.

        Parameters:
        start: Start time (server time in epoch milliseconds, UTC).

        stop: Stop time (server time in epoch milliseconds, UTC). If not specified
        default to time of latest server event available.

        count: Number of events to return. If not specified, return all events.

        stream_ids: Comma separated string of stream IDs. If specified, only retrieve events
        for listed streams.

        event_types: Comma servers string of event types. If specified, only retrieve the
        listed event types.
        """
        query_params = self._generate_event_query_params(start, stop, count, stream_ids, event_types)
        return self._get(f'/events/camera-stream?{query_params}')

    def get_camera_stream_event_histogram(self, start, stop, min_segment, stream_ids=None, event_types=None):
        """Get camera stream event histogram.

        Parameters:
        start: Start time (server time in epoch milliseconds, UTC).

        stop: Stop time (server time in epoch milliseconds, UTC).

        min_segment: Segment size of binned results.

        stream_ids: Comma separated string of stream IDs. If specified, only retrieve events
        for listed streams.

        event_types: Comma servers string of event types. If specified, only retrieve the
        listed event types.
        """
        query_params = f'start={start}&stop={stop}&minSegment={min_segment}'
        if stream_ids:
            query_params += f'&id={stream_ids}'
        if event_types:
            query_params += f'&type={event_types}'
        return self._get(f'/events/camera-stream/histogram?{query_params}')

    ### Logs Services

    def get_server_logs(self, log_format='gzip', start=None, stop=None):
        """Get server logs.

        Parameters:
        log_format: Log file format: [gzip, text].

        start: Start time (server time in epoch milliseconds, UTC).
        If not specified, use start time of earliest server log file.

        stop: Stop time (server time in epoch milliseconds, UTC).
        If not specified, use stop time of the latest server log file.
        """
        query_params = f'format={log_format}'
        if start:
            query_params += f'&from={start}'
        if stop:
            query_params += f'&to={stop}'
        return self._get(f'/log?{query_params}')

    ### User Services

    def get_users(self):
        """Get all users."""
        return self._get('/users')

    def create_user(self, username, password, role='Manager'):
        """Create a new user.

        Parameters:
        username: Name of new user.

        password: Password for new user.

        role: Permission scope: [Administrator, Manager, Live Viewer, Viewer].
        """
        body = {
            'username': username,
            'password': password,
            'role': role
            }
        return self._post('/users', body)

    def get_user(self, user_id):
        """Get a user by ID.

        Parameters:
        user_id: ID of user to retrieve.
        """
        return self._get(f'/users/{user_id}')

    def update_user(self, user_id, body):
        """Update a user (full update).

        Parameters:
        user_id: ID of user to update.

        body: User resource body.
        """
        return self._put(f'/users/{user_id}', body)

    def patch_user(self, user_id, body):
        """Patch a user (partial update).

        Parameters:
        user_id: ID of user to update.

        body: User resource body.
        """
        return self._patch(f'/users/{user_id}', body)

    def delete_user(self, user_id):
        """Delete a user.

        Parameters:
        user_id: ID of user to delete.
        """
        return self._delete(f'/users/{user_id}')

    ### Server Services

    def get_servers(self):
        """List all servers."""
        return self._get('/servers')

    def get_server(self, server_id=1):
        """Get a server by ID.

        Parameters:
        server_id: ID of server to retrieve.
        """
        return self._get(f'/servers/{server_id}')

    def generate_server_report(self, start, stop):
        """Generate a server report.

        Parameters:
        start: Start time (server time in epoch milliseconds, UTC).

        stop: Stop time (server time in epoch milliseconds, UTC).
        """
        return self._get(f'/server/report?start={start}&stop={stop}')

    def get_server_disk_utilization(self):
        """Get the server disk utilization."""
        return self._get('/server/utilization/disk')

    def get_server_database_faults(self, start, stop=None):
        """Get the server's database errors.

        Parameters:
        start: Start time (server time in epoch milliseconds, UTC).

        stop: Stop time (server in epoch milliseconds, UTC). If not specified.
        All database faults after start time will be retrieved.
        """
        query_params = f'start={start}'
        if stop:
            query_params += f'&stop={stop}'
        return self._get(f'/server/database-faults?{query_params}')

    ### Server Properties Services

    def get_server_properties_info(self):
        """Get information on configurable server properites."""
        return self._get('/server/properties/info')

    def get_server_properties(self):
        """Get the properties the server is currently configured with."""
        return self._get('/server/properties')

    def update_server_properties(self, body):
        """Update the server properties file.

        Parameters:
        body: Server properties resource body.
        """
        return self._put('/server/properties', body)

    def check_properties_confirmation(self):
        """Check if changes made to the properties file needs confirmation."""
        return self._get('/server/properties/confirmed')

    def confirm_properties(self, confirmed=True):
        """Confirm changes made to the properties file.

        Parameters:
        confirmed: If true, confirm the properties. Otherwise the
        server will revert to the previously configured settings.
        """
        body = { 'propertiesConfirmed': confirmed }
        return self._post('/server/properties/confirmed', body)

    ### Storage Services

    def get_storages(self):
        """List all archive storage locations."""
        return self._get('/storages')

    def get_storage(self, storage_id=1):
        """List an archive storage location by ID.

        Parameters:
        storage_id: ID of storage location to retrieve.
        """
        return self._get(f'/storages/{storage_id}')

    ### License Session Services

    def get_license_session(self):
        """Get the current Orchid VMS license session."""
        return self._get('/license-session')

    def create_license_session(self, orchid_license):
        """Create a new license session.

        Parameters:
        orchid_license: New Orchid Core VMS license to upload.
        """
        body = { 'license': orchid_license }
        return self._post('/license-session', body)

    def delete_license_session(self):
        """Delete the current license session."""
        return self._delete('/license-session')

    ### Endpoints Services

    def get_endpoints(self):
        """Get all Orchid Core VMS API endpoints."""
        return self._get('/endpoints')

    ### Version Services

    def get_version(self):
        """Get version information for Orchid Core VMS install."""
        return self._get('/version')

    ### User Interface Services

    def upload_ui_package(self, ui_package: bytes):
        """Upload a signed user-interface (UI) update package.

        Parameters:
        ui_package: ZIP package in bytes to upload. Note that this package must be
        signed by IPConfigure, Inc.
        """
        return self._post('/ui', ui_package)

    ### Internal Utility

    def _request(self, method, path, data=None):
        """Internal: Make an HTTP request

        This adds an extra `body` member to the `request.Response` object,
        which is automatically typed based on the response content-type:
          dict  -> application/json
          str   -> any text-based content-type
          bytes -> anything that is not of the previous two

        Parameters:
        method: HTTP method.

        path: Endpoint path.

        data: Request body data.
        """
        response = self.session.request(method, f'{self.server_address}/service/{path.lstrip("/")}',
                                        data=data, timeout=self.connection_timeout)
        content_type = response.headers['Content-Type']
        if 'application/json' in content_type:
            response.body = response.json()
        elif 'text' in content_type:
            response.body = response.text
        else: # raw bytes
            response.body = response.content
        return response

    def _get(self, path):
        """Internal: HTTP GET"""
        return self._request('GET', path)

    def _put(self, path, body=None):
        """Internal: HTTP PUT"""
        if isinstance(body, dict):
            body = json.dumps(body)
        return self._request('PUT', path, data=body)

    def _post(self, path, body=None):
        """Internal: HTTP POST"""
        if isinstance(body, dict):
            body = json.dumps(body)
        return self._request('POST', path, data=body)

    def _patch(self, path, body=None):
        """Internal: HTTP PATCH"""
        if isinstance(body, dict):
            body = json.dumps(body)
        return self._request('PATCH', path, data=body)

    def _delete(self, path):
        """Internal: HTTP DELETE"""
        return self._request('DELETE', path)

    @staticmethod
    def _generate_cam_registration_body(uri, username, password, name, driver):
        """Internal: Generate request body for registering new cameras"""
        body = {
            'driver': driver,
            'name': name,
            'connection': {
                'uri': uri,
                'username': username,
                'password': password
                }
            }
        return body

    @staticmethod
    def _generate_event_query_params(start, stop, count, ids, event_types):
        """Internal: Generate query parameters used for event services"""
        query_params = f'start={start}'
        if stop:
            query_params += f'&stop={stop}'
        if count:
            query_params += f'&count={count}'
        if ids:
            query_params += f'&id={ids}'
        if event_types:
            query_params += f'&eventType={event_types}'
        return query_params
