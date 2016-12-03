from configman import RequiredConfig, Namespace, converters


converters = converters


class ConfigurableComponent(RequiredConfig):

    required_config = Namespace()

    config = None
    component = None  # To store the component itself inside its configurator
    all_configurators = []  # This is used by the backend to start them all

    def __init__(self, config, local_config):
        self.config = local_config
        # Register configurator instance
        ConfigurableComponent.all_configurators.append(self)

    @classmethod
    def configure_component(cls, config, local_config):
        """
        This is a class method to either return an instance that already exists or create one.
        :param config:
        :param local_config:
        :return: Instance of ConfigurableComponent
        """
        return cls(config=config, local_config=local_config)

    def start(self):
        pass

    def stop(self):
        pass
