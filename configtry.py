
from configman import RequiredConfig, ConfigurationManager, Namespace, environment, ConfigFileFutureProxy, \
    command_line, converters
from ebu_tt_live.config.node import UniversalNode
from ebu_tt_live.config.backend import UniversalBackend
from ebu_tt_live.scripts.common import create_loggers


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

    backend = config.backend.type(config, config.backend)
    config.node.type(config, config.node)
    backend.start()

if __name__ == '__main__':
    main()
