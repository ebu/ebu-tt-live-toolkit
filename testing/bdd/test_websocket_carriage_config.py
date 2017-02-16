
from pytest_bdd import scenarios, given, when
import socket


scenarios('features/config/websocket_carriage_config.feature')


@given('a config file <config_file>')
def given_a_config_file(config_file):
    pass


@when('a free port has been found')
def when_an_ephemeral_port_is_found(template__dict):
    sock = socket.socket()
    sock.bind(('', 0))
    template__dict['ephemeral_port'] = sock.getsockname()[1]
    sock.close()
