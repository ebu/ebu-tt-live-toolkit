
import argparse
from configman import Namespace, ConfigurationManager, ConfigFileFutureProxy, command_line, environment, \
    RequiredConfig, dotdict


class ConfigurableOutput(RequiredConfig):
    pass


class ConsoleOutput(ConfigurableOutput):

    required_config = Namespace()

    def __init__(self, config, local_config):
        super(ConsoleOutput, self).__init__()
        self.config = local_config


class WebSocketOutput(ConfigurableOutput):

    required_config = Namespace()
    required_config.output_opts = output_opts = Namespace()
    output_opts.add_option('ws_uri', default='ws://localhost:9000')
    output_opts.add_option('ws_channel', default='TestSequence1')

    def __init__(self, config, local_config):
        super(WebSocketOutput, self).__init__()
        self.config = local_config


def output_factory(config, local_config, args):
    output_type = local_config.output_type
    if output_type == 'console':
        return ConsoleOutput(config, local_config)
    elif output_type == 'websocket':
        return WebSocketOutput(config, local_config)


class ConfigurableNode(RequiredConfig):
    pass


class OutputNode(ConfigurableNode):

    required_config = Namespace()



class SimpleProducer(RequiredConfig):

    required_config = Namespace()
    required_config.add_option('reference_clock', default=False)
    required_config.add_option(
        'output_type',
        default='console'
    )
    required_config.add_aggregation(
        name='output',
        function=output_factory
    )
    required_config.ref_value_namespace()

    def __init__(self, config):
        super(SimpleProducer, self).__init__()
        self.config = config
        self.output = self.config.output



def node_factory(config, local_config, args):
    node_type = local_config.node_type
    if node_type == "simple_producer":
        return SimpleProducer(config, local_config)


def universal_node():

    required_config = Namespace('Universal node')
    required_config.add_option(
        'node_type',
        default=SimpleProducer
    )

    return required_config


def create_config():

    config_manager = ConfigurationManager(
        definition_source=[
            universal_node()
        ],
        values_source_list=[ConfigFileFutureProxy, environment, command_line],
        app_name='Universal Nodes'
    )
    return config_manager


def main():
    config_manager = create_config()

    with config_manager.context() as config:
        node = config.node_type(config)
        print node

    #app = config.app_class(config)
