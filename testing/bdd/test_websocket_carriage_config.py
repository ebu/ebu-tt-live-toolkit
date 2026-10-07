import os
import socket

from jinja2 import Environment, FileSystemLoader
from pytest import fixture
from pytest_bdd import given, parsers, scenarios, then, when

from testing.bdd.conftest import legacy_name

scenarios('features/config/websocket_carriage_config.feature')


@fixture
def config_dict():
    return {}


@given(**legacy_name(name='a configuration file <config_file>'))
@given(
    name=parsers.parse(name='a configuration file {config_file}'),
    target_fixture='config_file')
def given_config_file(config_file):
    config_file = config_file.strip('"')
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(
        loader=FileSystemLoader(
            os.path.join(cur_dir, 'templates')),
        trim_blocks=True)
    return j2_env.get_template(config_file)


@when('the configuration file is loaded')
def when_config_loaded(config_file, config_dict):
    full_config = config_file.render(config_dict)


@when('a free port has been found')
def when_an_ephemeral_port_is_found(template_dict):
    sock = socket.socket()
    sock.bind(('', 0))
    template_dict['ephemeral_port'] = sock.getsockname()[1]
    sock.close()


@when('the producer listens on the port')
def when_producer_listens_port():
    pass


@when(**legacy_name(
    name='the consumer connects to the port with <client_url_path>'))
def when_consumer_connects_port(client_url_path):
    pass


@when(**legacy_name(name='producer sends document with <sequence_number_1>'))
def when_producer_sends_document1(sequence_number_1):
    pass


@when(**legacy_name(name='producer sends document with <sequence_number_2>'))
def when_producer_sends_document2(sequence_number_2):
    pass


@then('transmission should be successful')
def then_transmission_successful():
    pass
