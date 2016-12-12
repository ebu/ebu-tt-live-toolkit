from configman import RequiredConfig, Namespace, converters
from ebu_tt_live.strings import ERR_CONF_ONE_BACKEND_ONLY
from ebu_tt_live.errors import ConfigurationError


converters = converters


class ConfigurableComponent(RequiredConfig):

    required_config = Namespace()

    config = None
    component = None  # To store the component itself inside its configurator
    _backend = None  # Static variable holding the backend

    def __init__(self, config, local_config, backend=None):
        self.config = local_config

        if backend is not None:
            if self.backend is not None:
                raise ConfigurationError(
                    ERR_CONF_ONE_BACKEND_ONLY.format(
                        backend1=self.backend,
                        backend2=backend
                    )
                )
            else:
                ConfigurableComponent._backend = backend
        elif self.backend is not None:
            # Register configurator instance
            self.backend.register_configurator(self)

    @property
    def backend(self):
        return ConfigurableComponent._backend

    @classmethod
    def configure_component(cls, config, local_config, **kwargs):
        """
        This is a class method to either return an instance that already exists or create one.
        :param config:
        :param local_config:
        :param kwargs: Extra parameters
        :return: Instance of ConfigurableComponent
        """
        return cls(config=config, local_config=local_config)

    def start(self):
        pass

    def stop(self):
        pass
