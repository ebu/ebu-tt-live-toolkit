import logging
from .common import ConfigurableComponent, Namespace, RequiredConfig

log = logging.getLogger(__name__)


class BackendBase(ConfigurableComponent):

    _components_to_start = None
    _all_components = None

    def __init__(self, config, local_config):
        super(BackendBase, self).__init__(config, local_config, backend=self)
        self._components_to_start = []
        self._all_configurators = set()

    def register_configurator(self, configurator):
        self._all_configurators.add(configurator)

    def start(self):
        for item in self._all_configurators:
            # Start all the components
            if item != self and item in self._components_to_start:
                log.info('Starting component: {}'.format(item))
                item.start()

    def register_component_start(self, component):
        self._components_to_start.append(component)

    def call_once(self, func, delay=0.0, result_callback=None, error_callback=None, *args, **kwargs):
        raise NotImplementedError()

    def call_periodically(self, func, interval=0.0, result_callback=None, error_callback=None, *args, **kwargs):
        raise NotImplementedError()


class DummyBackend(BackendBase):

    _simple_calls = None
    _periodic_calls = None

    def __init__(self, config, local_config):
        self._simple_calls = []
        self._periodic_calls = []
        super(DummyBackend, self).__init__(config=config, local_config=local_config)

    def call_once(self, func, delay=0.0, result_callback=None, error_callback=None, *args, **kwargs):
        self._simple_calls.append({
            'func': func,
            'delay': delay,
            'result_callback': result_callback,
            'error_callback': error_callback
        })

    def call_periodically(self, func, interval=0.0, result_callback=None, error_callback=None, *args, **kwargs):
        self._periodic_calls.append({
            'func': func,
            'interval': interval,
            'result_callback': result_callback,
            'error_callback': error_callback
        })


class TwistedBackend(BackendBase):
    required_config = Namespace()

    _websocket = None
    _reactor = None
    _task = None

    _ws_twisted_producer_type = None
    _ws_twisted_consumer_type = None
    _wsl_twisted_producer_type = None
    _wsl_twisted_consumer_type = None
    _ws_twisted_producers = None
    _ws_twisted_consumers = None
    _ws_twisted_servers = None

    def __init__(self, config, local_config):
        from ebu_tt_live.twisted import websocket, reactor, task, TwistedWSPushProducer, TwistedWSConsumer, \
            TwistedConsumer, TwistedPullProducer
        self._websocket = websocket
        self._reactor = reactor
        self._task = task
        self._ws_twisted_producer_type = TwistedWSPushProducer
        self._wsl_twisted_producer_type = TwistedPullProducer
        self._ws_twisted_consumer_type = TwistedWSConsumer
        self._wsl_twisted_consumer_type = TwistedConsumer

        self._ws_twisted_servers = {}
        super(TwistedBackend, self).__init__(config=config, local_config=local_config)

    def start(self):
        super(TwistedBackend, self).start()
        self._reactor.run()

    def ws_backend_producer(self, uri, custom_producer):
        if uri not in self._ws_twisted_servers:
            twisted_producer = self._ws_twisted_producer_type(
                custom_producer=custom_producer
            )
            factory = self._websocket.BroadcastServerFactory(
                uri.geturl(),
                producer=twisted_producer
            )
            factory.protocol = self._websocket.BroadcastServerProtocol
            self._ws_twisted_servers[uri] = factory
            factory.listen()
        else:
            factory = self._ws_twisted_servers.get(uri)

        return factory.producer

    def wsl_backend_producer(self, uri, custom_producer):
        if uri not in self._ws_twisted_servers:
            twisted_producer = self._wsl_twisted_producer_type(
                custom_producer=custom_producer
            )
            factory = self._websocket.LegacyBroadcastServerFactory(
                uri.geturl()
            )
            factory.protocol = self._websocket.LegacyBroadcastServerProtocol
            factory.registerProducer(twisted_producer, streaming=True)
            self._ws_twisted_servers[uri] = factory
            factory.listen()
        else:
            factory = self._ws_twisted_servers.get(uri)

        return factory.producer

    def ws_backend_consumer(self, uri, custom_consumer, proxy=None):
        factory_args = {}
        if proxy:
            proxyHost, proxyPort = proxy.split(':')
            factory_args['proxy'] = {'host': proxyHost, 'port': int(proxyPort)}
        factory = self._websocket.BroadcastClientFactory(
            url=uri.geturl(),
            consumer=self._ws_twisted_consumer_type(
                custom_consumer=custom_consumer
            ),
            **factory_args
        )

        factory.protocol = self._websocket.BroadcastClientProtocol

        factory.connect()

    def wsl_backend_consumer(self, uri, custom_consumer, proxy=None):
        factory_args = {}
        if proxy:
            proxyHost, proxyPort = proxy.split(':')
            factory_args['proxy'] = {'host': proxyHost, 'port': int(proxyPort)}
        factory = self._websocket.LegacyBroadcastClientFactory(
            url=uri.geturl(),
            consumer=self._wsl_twisted_consumer_type(
                custom_consumer=custom_consumer
            ),
            **factory_args
        )

        factory.protocol = self._websocket.LegacyBroadcastClientProtocol

        factory.connect()

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
    elif backend_name == 'dummy':
        return DummyBackend
    else:
        raise Exception('No such component: {}'.format(backend_name))


class UniversalBackend(RequiredConfig):
    required_config = Namespace()
    required_config.backend = backend = Namespace()
    backend.add_option('type', default='twisted', from_string_converter=backend_by_type)
