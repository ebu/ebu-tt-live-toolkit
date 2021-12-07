import os
from jinja2 import Environment, FileSystemLoader
from pytest_bdd import scenarios, given, when, then, parsers
from pytest import fixture
import socket


scenarios('features/config/websocket_carriage_config.feature')


@fixture
def config_dict():
    return dict()


@given(parsers.parse('a configuration file {config_file}'), target_fixture='given_config_file')
def given_config_file(config_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
                         trim_blocks=True)
    return j2_env.get_template(config_file)


@when('the configuration file is loaded')
def when_config_loaded(given_config_file, config_dict):
    full_config = given_config_file.render(config_dict)


@when('a free port has been found')
def when_an_ephemeral_port_is_found(template_dict):
    sock = socket.socket()
    sock.bind(('', 0))
    template_dict['ephemeral_port'] = sock.getsockname()[1]
    sock.close()


@when('the producer listens on the port')
def when_producer_listens_port():
    pass


@when(parsers.parse('the consumer connects to the port with {client_url_path}'))
def when_consumer_connects_port(client_url_path):
    pass


@when(parsers.parse('producer sends document with {sequence_number_1}'))
def when_producer_sends_document1(sequence_number_1):
    pass


@when(parsers.parse('producer sends document with {sequence_number_2}'))
def when_producer_sends_document2(sequence_number_2):
    pass


@then('transmission should be successful')
def then_transmission_successful():
    pass
