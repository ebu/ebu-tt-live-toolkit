
from configman import RequiredConfig, ConfigurationManager, Namespace, environment, ConfigFileFutureProxy, \
    command_line, converters
from ebu_tt_live.config.node import SimpleProducer, SimpleConsumer
from ebu_tt_live.config.backend import TwistedBackend
from ebu_tt_live.scripts.common import create_loggers


def nodes_by_name(node_name):
    if node_name == 'simple-consumer':
        return SimpleConsumer
    elif node_name == 'simple-producer':
        return SimpleProducer
    else:
        raise Exception('No such node {}'.format(node_name))


class UniversalNode(RequiredConfig):
    required_config = Namespace()
    required_config.node = node = Namespace()
    node.add_option('type', default='simple-consumer', from_string_converter=nodes_by_name)


def backend_by_type(backend_name):
    if backend_name == 'twisted':
        return TwistedBackend
    else:
        raise Exception('No such component: {}'.format(backend_name))


class UniversalBackend(RequiredConfig):
    required_config = Namespace()
    required_config.backend = backend = Namespace()
    backend.add_option('type', default='twisted', from_string_converter=backend_by_type)


def main():
    create_loggers()
    cm = ConfigurationManager(
        definition_source=[
            UniversalNode.get_required_config(),
            UniversalBackend.get_required_config()
        ],
        values_source_list=[
            ConfigFileFutureProxy,
            command_line
        ]
    )
    config = cm.get_config()

    #node = config.node.type.configure(config.node)

    node = config.node.type.configure(config, config.node)
    print node
    backend = config.backend.type.configure(config, config.backend)
    print backend
    backend.start()

if __name__ == '__main__':
    main()
