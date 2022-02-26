# Testing

### Prerequisite
In order to run these tests, you need an [Orchid Core VMS installation](https://www.ipconfigure.com/products/orchid#download). It is recommended to use the latest version available.

### Getting started
Once Orchid is installed, copy the `settings.ini.template` into this directory like so (note the file must be named `settings.ini`):
```
$ cp templates/settings.ini.template settings.ini
```

Then edit the file with the correct credentials, for example:
```
[server]
uri=http://192.168.1.231
user=admin
password=P@ssword
```

### Running tests
```
$ cd <path/to/OrchidAPI>
$ pytest tests
======================================= test session starts ========================================
platform linux -- Python 3.8.10, pytest-7.0.1, pluggy-1.0.0
rootdir: /home/adavidson/devel/OrchidAPI, configfile: setup.cfg, testpaths: tests
plugins: cov-3.0.0
collected 8 items                                                                                  

tests/test_response_type.py ...                                                              [ 37%]
tests/test_sessions.py ....                                                                  [ 87%]
tests/test_trivial.py .                                                                      [100%]

======================================== 8 passed in 1.21s =========================================
```

Or if you prefer running from within `tests` directory:
```
$ cd tests
$ pytest --quiet .
........                                                                                     [100%]
8 passed in 1.24s
```

#### Coverage
```
$ cd <path/to/OrchidAPI>
$ coverage run --source=orchid_api -m pytest -q && coverage report
........                                                                                     [100%]
8 passed in 1.21s
Name                     Stmts   Miss Branch BrPart  Cover
----------------------------------------------------------
orchid_api/__init__.py     270     77     46     13    68%
----------------------------------------------------------
TOTAL                      270     77     46     13    68%
```
