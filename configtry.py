
from configman import RequiredConfig, ConfigurationManager, Namespace, environment, ConfigFileFutureProxy, \
    command_line, converters












class UniversalNode(RequiredConfig):
    required_config = Namespace()
    required_config.node = node = Namespace()
    node.add_option('type', default='simple-consumer', from_string_converter=converters.class_converter)


def main():
    cm = ConfigurationManager(
        definition_source=[
            UniversalNode.get_required_config()
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


if __name__ == '__main__':
    main()
