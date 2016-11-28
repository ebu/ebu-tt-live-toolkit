from configman import RequiredConfig, Namespace, converters


class ConfigurableComponent(RequiredConfig):

    required_config = Namespace()

    component = None  # To store the component itself inside its configurator

    def __init__(self, config, local_config):
        self.config = local_config
