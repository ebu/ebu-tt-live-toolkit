
from configman import RequiredConfig, ConfigurationManager, Namespace, environment, ConfigFileFutureProxy, \
    command_line, converters
from ebu_tt_live.config.node import UniversalNodes
from ebu_tt_live.config.backend import UniversalBackend
from ebu_tt_live.scripts.common import create_loggers


def main():
    create_loggers()
    cm = ConfigurationManager(
        definition_source=[
            UniversalNodes.get_required_config(),
            UniversalBackend.get_required_config()
        ],
        values_source_list=[
            ConfigFileFutureProxy,
            command_line
        ]
    )
    config = cm.get_config()

    backend = config.backend.type.configure_component(config, config.backend)
    uni_nodes = config.nodes.type.configure_component(config, config.nodes)
    backend.start()

if __name__ == '__main__':
    main()
