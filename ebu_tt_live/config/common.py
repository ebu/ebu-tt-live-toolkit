from configman import RequiredConfig, Namespace, converters


class ConfigurableComponent(RequiredConfig):

    required_config = Namespace()

    component = None  # To store the component itself inside its configurator
    all_configurators = []  # This is used by the backend to start them all

    def __init__(self, config, local_config):
        self.config = local_config
        # Register configurator instance
        ConfigurableComponent.all_configurators.append(self)

    def start(self):
        pass

    def stop(self):
        pass
