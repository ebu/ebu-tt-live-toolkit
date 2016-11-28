from .common import ConfigurableComponent, Namespace, RequiredConfig

current_backend = None


class BackendBase(ConfigurableComponent):

    components_to_start = None

    def __init__(self, config, local_config):
        super(BackendBase, self).__init__(config, local_config)
        self.components_to_start = []
        global current_backend
        current_backend = self

    def start(self):
        raise NotImplementedError()

    def register_component_start(self, component):
        self.components_to_start.append(component)


class TwistedBackend(BackendBase):
    required_config = Namespace()

    def __init__(self, config, local_config):
        super(TwistedBackend, self).__init__(config, local_config)

    def start(self):
        from twisted.internet import reactor
        for item in ConfigurableComponent.all_configurators:
            # Start all the components
            if item != self:
                item.start()
        reactor.run()


def backend_by_type(backend_name):
    if backend_name == 'twisted':
        return TwistedBackend
    else:
        raise Exception('No such component: {}'.format(backend_name))


class UniversalBackend(RequiredConfig):
    required_config = Namespace()
    required_config.backend = backend = Namespace()
    backend.add_option('type', default='twisted', from_string_converter=backend_by_type)