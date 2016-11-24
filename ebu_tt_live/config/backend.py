from .common import ConfigurableComponent, Namespace


class BackendBase(ConfigurableComponent):

    def start(self):
        raise NotImplementedError()


class TwistedBackend(BackendBase):
    required_config = Namespace()

    def start(self):
        from twisted.internet import reactor
        reactor.run()
