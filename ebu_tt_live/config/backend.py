import logging
from .common import ConfigurableComponent, Namespace, RequiredConfig

log = logging.getLogger(__name__)


class BackendBase(ConfigurableComponent):

    _components_to_start = None

    def __init__(self, config, local_config):
        super(BackendBase, self).__init__(config, local_config, backend=self)
        self._components_to_start = []

    def start(self):
        raise NotImplementedError()

    def register_component_start(self, component):
        self._components_to_start.append(component)


class TwistedBackend(BackendBase):
    required_config = Namespace()

    _websocket = None
    _reactor = None
    _task = None

    _ws_twisted_producer_type = None
    _ws_twisted_consumer_type = None
    _ws_twisted_producers = None
    _ws_twisted_consumers = None

    def __init__(self, config, local_config):
        from ebu_tt_live.twisted import websocket, reactor, task, TwistedPushProducer, TwistedConsumer
        self._websocket = websocket
        self._reactor = reactor
        self._task = task
        self._twisted_producer_type = TwistedPushProducer
        self._twisted_consumer_type = TwistedConsumer
        self._ws_twisted_servers = {}
        super(TwistedBackend, self).__init__(config=config, local_config=local_config)

    def start(self):
        for item in ConfigurableComponent.all_configurators:
            # Start all the components
            if item != self and item in self._components_to_start:
                log.info('Starting component: {}'.format(item))
                item.start()
        self._reactor.run()

    def ws_backend_producer(self, uri, custom_producer):
        if uri not in self._ws_twisted_servers:
            factory = self._websocket.BroadcastServerFactory(uri.geturl())
            factory.protocol = self._websocket.BroadcastServerProtocol
            self._ws_twisted_servers[uri] = factory
            factory.listen()
        else:
            factory = self._ws_twisted_servers.get(uri)

        twisted_producer = self._twisted_producer_type(
            consumer=factory,
            custom_producer=custom_producer
        )

        return twisted_producer

    def ws_backend_consumer(self, uri, custom_consumer):
        return None

    def call_once(self, func, delay=0.0, result_callback=None, error_callback=None, *args, **kwargs):
        d = self._task.deferLater(self._reactor, delay=delay, callable=func, *args, **kwargs)
        if result_callback is not None:
            d.addCallback(result_callback)
        if error_callback is not None:
            d.addErrback(error_callback)

    def call_periodically(self, func, interval=0.0, result_callback=None, error_callback=None, *args, **kwargs):
        looping_call = self._task.LoopingCall(f=func, *args, **kwargs)
        d = looping_call.start(interval, now=False)
        if result_callback is not None:
            d.addCallback(result_callback)
        if error_callback is not None:
            d.addErrback(error_callback)


def backend_by_type(backend_name):
    if backend_name == 'twisted':
        return TwistedBackend
    else:
        raise Exception('No such component: {}'.format(backend_name))


class UniversalBackend(RequiredConfig):
    required_config = Namespace()
    required_config.backend = backend = Namespace()
    backend.add_option('type', default='twisted', from_string_converter=backend_by_type)
