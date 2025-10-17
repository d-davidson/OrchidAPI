# OrchidAPI
`OrchidAPI` is a lightweight, easy-to-use API wrapper designed for streamlining automated tasks with an [Orchid Core VMS](https://www.ipconfigure.com).

See:
- [OrchidAPI documentation](doc.md)
- [Orchid Core VMS API documentation](https://orchid.ipconfigure.com/api).

# Installing
Currently only local installation is supported (this library has not been uploaded to PyPI, yet).
```
pip3 install <path/to/OrchidAPI>
```

# Simple Example
```python
from orchid_api import OrchidAPI

api = OrchidAPI('https://your-orchid-server:8443', user='thunder', password='P@ssword')

if api.patch('/cameras/1', {'name': 'New camera name'}).status_code == 200:
    print(api.get('/cameras/1').json()['name'])
```
