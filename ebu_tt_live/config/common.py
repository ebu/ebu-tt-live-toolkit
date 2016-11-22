from configman import RequiredConfig, Namespace, converters


class ConfigurableComponent(RequiredConfig):

    required_config = Namespace()

    @classmethod
    def configure(cls, config, local_config):
        instance = cls()
        instance.config = local_config
        return instance
