from configparser import ConfigParser
from pathlib import Path

setup_ini = Path(__file__).parent / 'setup.ini'
assert setup_ini.exists(), f'Setup file is mandatory: {setup_ini}'

config = ConfigParser()
config.read(setup_ini)

assert 'server' in config, 'Section [server] in test configuration is mandatory'
server_config = config['server']

if 'camera' in config:
    cam_config = config['camera']
