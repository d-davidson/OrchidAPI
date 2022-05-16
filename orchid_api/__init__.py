"""OrchidAPI: Orchid Core VMS API wrapper.

This library is implemented in accordance with the Orchid Core VMS
API documentation: https://orchid.ipconfigure.com/api/.
"""

import json
import base64
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

    ### Time Services

    def get_server_time(self, extended: bool=True) -> requests.Response:
        """Get the Orchid Core VMS server time (in epoch milliseconds, UTC).

        Parameters:
        extended: If true, return extended response that includes timezone
        information. Otherwise, return epoch timestamp only.
        """
        if extended:
            return self._get('/time-extended')
        return self._get('/time')

    ### Trusted Issuer Services

    def get_trusted_issuer(self) -> requests.Response:
        """Retrieve the current trusted issuer."""
        return self._get('/trusted/issuer')

    def create_trusted_issuer(self, orchid_uuid: str, secret: bytes,
                              description: str='', uri: str='') -> requests.Response:
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

    def delete_trusted_issuer(self) -> requests.Response:
        """Delete the trusted issuer."""
        return self._delete('/trusted/issuer')

    ### Sessions Services

    def get_session_identity(self) -> requests.Response:
        """Get the identity of current session."""
        return self._get('/identity')

    def get_session_info(self) -> requests.Response:
        """Get the current session information."""
        return self._get('/sessions/me')

    def delete_current_session(self) -> requests.Response:
        """Delete the current session."""
        return self._delete('/sessions/me')

    def create_user_session(self, username: str, password: str, expires_in: int=3600,
                            cookie: str='session') -> requests.Response:
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

    def create_remote_session(self, session_name: str, expires_in: int=3600,
                              cookie: str='session', scope: dict=None) -> requests.Response:
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

    def get_sessions(self, session_type: str=None) -> requests.Response:
        """Get all sessions associated to Orchid Core VMS server.

        Parameters:
        session_type: Session type filter: [user, remote].
        If not set, all session types are retrieved.
        """
        if session_type:
            return self._get(f'/sessions?type={session_type}')
        return self._get('/sessions')

    def delete_sessions(self, session_type: str=None) -> requests.Response:
        """Delete all sessions.

        Parameters:
        session_type: Session type filter: [user, remote].
        If not set, all session types are deleted.
        """
        if session_type:
            return self._delete(f'/sessions?type={session_type}')
        return self._delete('/sessions')

    def get_session(self, session_id: str) -> requests.Response:
        """Get a session by ID.

        Parameters:
        session_id: ID of the session to retrieve.
        """
        return self._get(f'/sessions?{session_id}')

    def delete_session(self, session_id: str) -> requests.Response:
        """Delete a session by ID.

        Parameters:
        session_id: ID of the session to delete.
        """
        return self._delete(f'/sessions?{session_id}')

    ### Discoverable Services

    def get_discovered_cameras(self) -> requests.Response:
        """Get all of the camera discovered via ONVIF autodiscovery."""
        return self._get('/discoverable/cameras')

    def get_orchids(self) -> requests.Response:
        """Get all the discovered Orchid Core VMS servers."""
        return self._get('/discoverable/orchids')

    def get_orchid(self, orchid_id: int=1) -> requests.Response:
        """Get a discovered Orchid Core VMS

        Parameters:
        orchid_id: ID of the Orchid Core VMS.
        """
        return self._get(f'/discoverable/orchids/{orchid_id}')

    ### Camera Services

    def get_cameras(self) -> requests.Response:
        """Get all registered cameras."""
        return self._get('/cameras')

    def register_onvif_camera(self, address: str, camera_user: str, password: str,
                              name: str=None, https: bool=False) -> requests.Response:
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

    def register_rtsp_camera(self, uri: str, camera_user: str,
                             password: str, name: str=None) -> requests.Response:
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

    def get_camera(self, camera_id: int) -> requests.Response:
        """Get a camera by ID.

        Parameters:
        camera_id: ID of camera to retrieve.
        """
        return self._get(f'/cameras/{camera_id}')

    def patch_camera(self, camera_id: int, body: dict) -> requests.Response:
        """Patch a camera (partial update).

        Parameters:
        camera_id: ID of camera to update.

        body: Camera resource PATCH body.
        """
        return self._patch(f'/cameras/{camera_id}', body)

    def delete_camera(self, camera_id: int) -> requests.Response:
        """Delete a camera.

        Parameters:
        camera_id: ID of camera to delete.
        """
        return self._delete(f'/cameras/{camera_id}')

    def verify_camera(self, camera_id: int) -> requests.Response:
        """Verify a camera is pingable.

        Parameters:
        camera_id: ID of camera to ping.
        """
        return self._get(f'/cameras/{camera_id}/verify')

    def get_cameras_disk_usage(self) -> requests.Response:
        """Get the archive disk usage of all cameras."""
        return self._get('/cameras/disk-usage')

    def get_tz_list(self):
        """Get a list if IANA to POSIX timezone mappings."""
        return self._get('/cameras/tz-list')

    def get_camera_ptz_position(self, camera_id: int) -> requests.Response:
        """Get a camera's current PTZ position.

        Parameters:
        camera_id: ID of camera to retrieve PTZ position for.
        """
        return self._get(f'/cameras/{camera_id}/position')

    def set_camera_ptz_position(self, camera_id: int, body: dict) -> requests.Response:
        """Set a camera's PTZ position.

        Parameters:
        camera_id: ID of camera to set PTZ position for.

        body: Camera PTZ resource body.
        """
        return self._post(f'/cameras/{camera_id}/position', body)

    def get_camera_ptz_presets(self, camera_id: int) -> requests.Response:
        """Get a list of a camera's PTZ presets.

        Parameters:
        camera_id: ID of camera to retrieve PTZ preset list for.
        """
        return self._get(f'/cameras/{camera_id}/position/presets')

    def set_camera_ptz_preset(self, camera_id: int, preset_name: str) -> requests.Response:
        """Set a camera's PTZ preset at the camera's current PTZ position.

        Parameters:
        camera_id: ID of camera to set PTZ preset for.

        preset_name: Name of preset.
        """
        body = { 'name': preset_name }
        return self._post(f'/cameras/{camera_id}/position/presets', body)

    def delete_camera_ptz_preset(self, camera_id: int, preset_token: str) -> requests.Response:
        """Delete the PTZ preset on a camera.

        Parameters:
        camera_id: ID of camera to delete PTZ preset for.

        preset_token: Token/ID of the PTZ preset to delete.
        """
        return self._delete(f'/cameras/{camera_id}/position/presets/{preset_token}')

    ### Stream Services

    def get_camera_streams(self, camera_id: int) -> requests.Response:
        """List all the stream's for a camera.

        Parameters:
        camera_id: ID of camera to retrieve streams for.
        """
        return self._get(f'/cameras/{camera_id}/streams')

    def register_stream(self, camera_id: int, body: dict) -> requests.Response:
        """Register a new stream for a camera.

        Parameters:
        camera_id: ID of camera to register a new stream for.

        body: Stream resource body.
        """
        return self._post(f'/cameras/{camera_id}/streams', body)

    def get_camera_stream(self, camera_id: int, stream_id: int) -> requests.Response:
        """Get a camera's stream.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to retrieve.
        """
        return self._get(f'/cameras/{camera_id}/streams/{stream_id}')

    def patch_stream(self, camera_id: int, stream_id: int, body: dict) -> requests.Response:
        """Patch a camera's stream (partial update).

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to update.

        body: Stream resource PATCH body.
        """
        return self._patch(f'/cameras/{camera_id}/streams/{stream_id}', body)

    def update_stream(self, camera_id: int, stream_id: int, body: dict) -> requests.Response:
        """Update a camera's stream (full update).

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to update.

        body: Stream resource body.
        """
        return self._put(f'/cameras/{camera_id}/streams/{stream_id}', body)

    def delete_stream(self, camera_id: int, stream_id: int) -> requests.Response:
        """Delete a camera's stream.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to delete.
        """
        return self._delete(f'/cameras/{camera_id}/streams/{stream_id}')

    def restart_stream(self, camera_id: int, stream_id: int) -> requests.Response:
        """Restart a camera stream.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to restart.
        """
        return self._patch(f'/cameras/{camera_id}/streams/{stream_id}/restart')

    def get_stream_motion_mask(self, camera_id: int, stream_id: int) -> requests.Response:
        """Get a camera stream's motion mask.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to get motion mask for
        """
        return self._get(f'/cameras/{camera_id}/streams/{stream_id}/motion/mask')

    def upload_stream_motion_mask(self, camera_id: int, stream_id: int,
                                  mask: bytes) -> requests.Response:
        """Upload a camera stream's motion mask.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to upload motion mask for.

        mask: PNG image of stream frame, in bytes, containing motion mask.
        """
        return self._put(f'/cameras/{camera_id}/streams/{stream_id}/motion/mask', mask)

    def delete_stream_motion_mask(self, camera_id: int, stream_id: int) -> requests.Response:
        """Delete a camera stream's motion mask.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to delete motion mask for.
        """
        return self._delete(f'/cameras/{camera_id}/streams/{stream_id}/motion/mask')

    def get_streams(self) -> requests.Response:
        """List all registered streams."""
        return self._get('/streams')

    def get_stream_statuses(self):
        """List the status of all registered streams."""
        return self._get('/streams/status')

    def get_stream(self, stream_id: int) -> requests.Response:
        """Get a stream.

        Parameters:
        stream_id: ID of stream to retrieve.
        """
        return self._get(f'/streams/{stream_id}')

    def get_stream_frame(self, stream_id: int, time: int=0, height: int=0,
                         width: int=0, fallback: bool=False) -> requests.Response:
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

    def export_stream(self, stream_id: int, start: int,
                      stop: int, container: str='mkv') -> requests.Response:
        """Export media from a stream.

        Parameters:
        stream_id: ID of stream to export media for.

        start: Start time (server time in epoch milliseconds, UTC).

        stop: Stop time (server time in epoch milliseconds, UTC).

        container: Video export format: [mkv, mov, mp4, dewarp, dewarp-parent].
        """
        return self._get(f'/streams/{stream_id}/export?start={start}&stop={stop}&format={container}')

    def get_stream_metadata(self, camera_id: int, stream_id: int) -> requests.Response:
        """Get a camera stream's metadata.

        Parameters:
        camera_id: ID of camera that stream is associated to.

        stream_id: ID of stream to retrieve metadata for.
        """
        return self._get(f'/cameras/{camera_id}/streams/{stream_id}/metadata')

    def get_stream_status(self, stream_id: int) -> requests.Response:
        """Get status of a stream.

        Parameters:
        stream_id: ID of stream to retrieve status for.
        """
        return self._get(f'/streams/{stream_id}/status')

    ### Archive Services

    def get_archives(self, start: int=0, take: int=100,
                     offset: int=0, stream_id: int=None) -> requests.Response:
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

    def get_archive(self, archive_id: int) -> requests.Response:
        """Get an archive by ID.

        Parameters:
        archive_id: ID of archive to retrieve.
        """
        return self._get(f'/archives/{archive_id}')

    def download_archive(self, archive_id: int) -> requests.Response:
        """Download an archive by ID.

        Parameters:
        archive_id: ID of archive to download.
        """
        return self._get(f'/archives/{archive_id}/download')

    def get_archives_per_day(self) -> requests.Response:
        """Get a count of archives generated, per day."""
        return self._get('/archives/per-day')

    ### Frame Puller Services

    def get_lbm_streams(self) -> requests.Response:
        """List all currently active low-bandwidth streams."""
        return self._get('/low-bandwidth/streams')

    def create_lbm_stream(self, stream_id: int, height: int, width: int,
                          start: int=0, sync: bool=False, rate: float=1.0,
                          wait_thres: int=2000, transport: str='websocket-base64') -> requests.Response:
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

    def get_lbm_stream(self, stream_uuid: str) -> requests.Response:
        """Get a low-bandwidth mode stream by ID.

        Parameters:
        stream_uuid: ID of low-bandwidth mode stream.
        """
        return self._get(f'/low-bandwidth/streams/{stream_uuid}')

    def delete_lbm_stream(self, stream_uuid: str) -> requests.Response:
        """Delete an LBM stream.

        Parameters:
        stream_uuid: ID of low-bandwidth mode stream to delete.
        """
        return self._delete(f'/low-bandwidth/streams/{stream_uuid}')

    def get_lbm_frame(self, stream_uuid: str) -> requests.Response:
        """Get a low-bandwidth mode stream JPEG frame from a session created for `http` mode.

        Parameters:
        stream_uuid: ID of low-bandwidth mode stream to get frame for.
        """
        return self._get(f'/low-bandwidth/streams/{stream_uuid}/frame')

    ### Event Services

    def get_server_events(self, start: int, stop: int=None, count: int=None,
                          server_ids: str=None, event_types: str=None) -> requests.Response:
        """Get server events.

        Parameters:
        start: Start time (server time in epoch milliseconds, UTC).

        stop: Stop time (server time in epoch milliseconds, UTC). If not specified
        default to time of latest server event available.

        count: Number of events to return. If not specified, return all events.

        server_ids: Comma separated string of server IDs. If specified, only retrieve events
        for listed servers.

        event_types: Comma separated string of event types. If specified, only retrieve the
        listed event types.
        """
        query_params = self._generate_event_query_params(start, stop, count, server_ids, event_types)
        return self._get(f'/events/server?{query_params}')

    def get_stream_events(self, start: int, stop: int=None, count: int=None,
                          stream_ids: int=None, event_types: int=None) -> requests.Response:
        """Get camera stream events.

        Parameters:
        start: Start time (server time in epoch milliseconds, UTC).

        stop: Stop time (server time in epoch milliseconds, UTC). If not specified
        default to time of latest server event available.

        count: Number of events to return. If not specified, return all events.

        stream_ids: Comma separated string of stream IDs. If specified, only retrieve events
        for listed streams.

        event_types: Comma separated string of event types. If specified, only retrieve the
        listed event types.
        """
        query_params = self._generate_event_query_params(start, stop, count, stream_ids, event_types)
        return self._get(f'/events/camera-stream?{query_params}')

    def get_camera_stream_event_histogram(self, start: int, stop: int, min_segment: int,
                                          stream_ids: str=None, event_types: str=None) -> requests.Response:
        """Get camera stream event histogram.

        Parameters:
        start: Start time (server time in epoch milliseconds, UTC).

        stop: Stop time (server time in epoch milliseconds, UTC).

        min_segment: Segment size of binned results.

        stream_ids: Comma separated string of stream IDs. If specified, only retrieve events
        for listed streams.

        event_types: Comma separated string of event types. If specified, only retrieve the
        listed event types.
        """
        query_params = f'start={start}&stop={stop}&minSegment={min_segment}'
        if stream_ids:
            query_params += f'&id={stream_ids}'
        if event_types:
            query_params += f'&type={event_types}'
        return self._get(f'/events/camera-stream/histogram?{query_params}')

    ### Logs Services

    def get_server_logs(self, log_format: str='gzip',
                        start: int=None, stop: int=None) -> requests.Response:
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

    def create_user(self, username: str, password: str,
                    role: str='Manager') -> requests.Response:
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

    def get_user(self, user_id: int) -> requests.Response:
        """Get a user by ID.

        Parameters:
        user_id: ID of user to retrieve.
        """
        return self._get(f'/users/{user_id}')

    def update_user(self, user_id: int, body: dict) -> requests.Response:
        """Update a user (full update).

        Parameters:
        user_id: ID of user to update.

        body: User resource body.
        """
        return self._put(f'/users/{user_id}', body)

    def patch_user(self, user_id: int, body: dict) -> requests.Response:
        """Patch a user (partial update).

        Parameters:
        user_id: ID of user to update.

        body: User resource body.
        """
        return self._patch(f'/users/{user_id}', body)

    def delete_user(self, user_id: int) -> requests.Response:
        """Delete a user.

        Parameters:
        user_id: ID of user to delete.
        """
        return self._delete(f'/users/{user_id}')

    ### Server Services

    def get_servers(self) -> requests.Response:
        """List all servers."""
        return self._get('/servers')

    def get_server(self, server_id: int=1) -> requests.Response:
        """Get a server by ID.

        Parameters:
        server_id: ID of server to retrieve.
        """
        return self._get(f'/servers/{server_id}')

    def generate_server_report(self, start: int, stop: int) -> requests.Response:
        """Generate a server report.

        Parameters:
        start: Start time (server time in epoch milliseconds, UTC).

        stop: Stop time (server time in epoch milliseconds, UTC).
        """
        return self._get(f'/server/report?start={start}&stop={stop}')

    def get_server_disk_utilization(self) -> requests.Response:
        """Get the server disk utilization."""
        return self._get('/server/utilization/disk')

    def get_server_database_faults(self, start: int, stop: int=None) -> requests.Response:
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

    def get_server_properties_info(self) -> requests.Response:
        """Get information on configurable server properites."""
        return self._get('/server/properties/info')

    def get_server_properties(self) -> requests.Response:
        """Get the properties the server is currently configured with."""
        return self._get('/server/properties')

    def update_server_properties(self, body: dict) -> requests.Response:
        """Update the server properties file.

        Parameters:
        body: Server properties resource body.
        """
        return self._put('/server/properties', body)

    def check_properties_confirmation(self) -> requests.Response:
        """Check if changes made to the properties file needs confirmation."""
        return self._get('/server/properties/confirmed')

    def confirm_properties(self, confirmed: bool=True) -> requests.Response:
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

    def get_storage(self, storage_id: int=1) -> requests.Response:
        """List an archive storage location by ID.

        Parameters:
        storage_id: ID of storage location to retrieve.
        """
        return self._get(f'/storages/{storage_id}')

    ### License Session Services

    def get_license_session(self) -> requests.Response:
        """Get the current Orchid VMS license session."""
        return self._get('/license-session')

    def create_license_session(self, orchid_license: str) -> requests.Response:
        """Create a new license session.

        Parameters:
        orchid_license: New Orchid Core VMS license to upload.
        """
        body = { 'license': orchid_license }
        return self._post('/license-session', body)

    def delete_license_session(self) -> requests.Response:
        """Delete the current license session."""
        return self._delete('/license-session')

    ### Endpoints Services

    def get_endpoints(self) -> requests.Response:
        """Get all Orchid Core VMS API endpoints."""
        return self._get('/endpoints')

    ### Version Services

    def get_version(self) -> requests.Response:
        """Get version information for Orchid Core VMS install."""
        return self._get('/version')

    ### User Interface Services

    def upload_ui_package(self, ui_package: bytes) -> requests.Response:
        """Upload a signed user-interface (UI) update package.

        Parameters:
        ui_package: ZIP package in bytes to upload. Note that this package must be
        signed by IPConfigure, Inc.
        """
        return self._post('/ui', ui_package)

    ### Internal Utility

    def _request(self, method: str, path: str, data: Union[dict, bytes]=None) -> requests.Response:
        """Internal: Make an HTTP request

        This adds an extra `body` member to the `requests.Response` object,
        which is automatically typed based on the response content-type:
          dict  -> application/json
          str   -> any text-based content-type
          bytes -> anything that is not of the previous two

        Parameters:
        method: HTTP method.

        path: Endpoint path.

        data: Request body data.
        """
        if isinstance(data, dict):
            data = json.dumps(data)
        response = self.session.request(method, f'{self.server_address}/service/{path.lstrip("/")}',
                                        data=data, timeout=self.timeout)
        content_type = response.headers['Content-Type']
        if 'application/json' in content_type:
            response.body = response.json()
        elif 'text' in content_type:
            response.body = response.text
        else: # raw bytes
            response.body = response.content
        return response

    def _get(self, path: str) -> requests.Response:
        """Internal: HTTP GET"""
        return self._request('GET', path)

    def _put(self, path: str, body: Union[dict, bytes]=None) -> requests.Response:
        """Internal: HTTP PUT"""
        return self._request('PUT', path, data=body)

    def _post(self, path: str, body: Union[dict, bytes]=None) -> requests.Response:
        """Internal: HTTP POST"""
        return self._request('POST', path, data=body)

    def _patch(self, path: str, body: dict=None) -> requests.Response:
        """Internal: HTTP PATCH"""
        return self._request('PATCH', path, data=body)

    def _delete(self, path: str) -> requests.Response:
        """Internal: HTTP DELETE"""
        return self._request('DELETE', path)

    @staticmethod
    def _generate_cam_registration_body(uri: str, username: str, password: str,
                                        name: str, driver: str) -> dict:
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
    def _generate_event_query_params(start: int, stop: int, count: int,
                                     ids: str, event_types: str) -> str:
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
