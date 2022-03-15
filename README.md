# OrchidAPI
`OrchidAPI` is a lightweight, easy-to-use API wrapper designed for streamlining automated tasks with an [Orchid Core VMS](https://www.ipconfigure.com/products/orchid).

See: [Orchid Core VMS API documentation](https://orchid.ipconfigure.com/api/).

# Installing
Currently only local installation is supported (this library has not been uploaded to PyPI, yet).
```
pip3 install <path/to/OrchidAPI>
```

# Simple Example
```python
from orchid_api import OrchidAPI

api = OrchidAPI('https://your-orchid-server:8443', user='thunder', password='P@ssword')

cam = api.get_camera(1).body
cam['name'] = 'New camera name'

resp = api.patch_camera(1, cam)
```
