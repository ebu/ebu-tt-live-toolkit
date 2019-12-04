import logging
from .common import ConfigurableComponent, Namespace, RequiredConfig
from ebu_tt_live.strings import ERR_CONF_WS_SERVER_PROTOCOL_MISMATCH
from ebu_tt_live.errors import ConfigurationError
from ebu_tt_live.strings import ERR_NO_SUCH_COMPONENT


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
        log.info(self._components_to_start)

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
    _wsl_twisted_servers = None
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

        self._wsl_twisted_servers = {}
        self._ws_twisted_servers = {}
        super(TwistedBackend, self).__init__(config=config, local_config=local_config)

    def start(self):
        super(TwistedBackend, self).start()
        self._reactor.run()

    def _crosscheck_ws_server_uri(self, listen, legacy=False):
        """
        Checking for sockets already listening on the specified listen address. If there is a server there
        its factory is returned, if there isn't one, None is returned, if there is protocol mismatch
        a ConfigurationError exception is raised.
        :param listen: URI of websocket server
        :return: BroadcastServerFactory instance if exists for listen address, otherwise None
        :raises ConfigurationError: on protocol mismatch
        """
        ws_server = self._ws_twisted_servers.get(listen)
        wsl_server = self._wsl_twisted_servers.get(listen)
        if ws_server and legacy or wsl_server and not legacy:
            raise ConfigurationError(
                ERR_CONF_WS_SERVER_PROTOCOL_MISMATCH.format(
                    address=listen
                )
            )
        if ws_server:
            return ws_server
        if wsl_server:
            return wsl_server
        return None

    def _ws_create_server_factory(self, listen, producer=None, consumer=None):
        server_factory = self._websocket.BroadcastServerFactory(
            listen.geturl(),
            producer=producer,
            consumer=consumer
        )
        server_factory.protocol = self._websocket.BroadcastServerProtocol
        self._ws_twisted_servers[listen.geturl()] = server_factory
        server_factory.listen()
        return server_factory

    def _ws_create_client_factories(self, connect, producer=None, consumer=None, proxy=None):
        factory_args = {}
        for dst in connect:
            client_factory = self._websocket.BroadcastClientFactory(
                url=dst.geturl(),
                producer=producer,
                consumer=consumer,
                **factory_args
            )
            client_factory.protocol = self._websocket.BroadcastClientProtocol
            client_factory.proxy = proxy

            client_factory.connect()

    def ws_backend_producer(self, custom_producer, listen=None, connect=None, proxy=None):
        """
        The following cases to be considered.
            1. There is listen address
                1.1. The address is used by another producer: ERROR
                1.2. The address is used by another protocol: ERROR
                1.3. The address is used by a consumer server: create producer and assign it to the factory
                1.4. The address is not in use: Create factory and create producer
            2. There are connections to make with *publish* action
                2.1 There is a producer from the server. Use that. Create client factories with it.
                2.2 There is no producer from the server. Create producer, create client factories with it.

        :param custom_producer:
        :param listen:
        :param connect:
        :param proxy:
        :return: The Twisted Producer instance with server socket and/or client connections
        """
        server_factory = listen and self._crosscheck_ws_server_uri(listen.geturl()) or None
        twisted_producer = server_factory and server_factory.producer or None
        if not twisted_producer:
            twisted_producer = self._ws_twisted_producer_type(
                custom_producer=custom_producer
            )

        if listen:
            if server_factory:
                server_factory.producer = twisted_producer
            else:
                self._ws_create_server_factory(
                    listen=listen,
                    producer=twisted_producer
                )

        if connect:
            self._ws_create_client_factories(
                connect=connect,
                producer=twisted_producer,
                proxy=proxy
            )

        return twisted_producer

    def ws_backend_consumer(self, custom_consumer, listen=None, connect=None, proxy=None):
        server_factory = listen and self._crosscheck_ws_server_uri(listen.geturl()) or None
        twisted_consumer = server_factory and server_factory.consumer or None

        if not twisted_consumer:
            twisted_consumer = self._ws_twisted_consumer_type(
                custom_consumer=custom_consumer
            )

        if listen:
            if server_factory:
                server_factory.consumer = twisted_consumer
            else:
                self._ws_create_server_factory(
                    listen=listen,
                    consumer=twisted_consumer
                )

        if connect:
            self._ws_create_client_factories(
                connect=connect,
                consumer=twisted_consumer,
                proxy=proxy
            )

        return twisted_consumer

    def wsl_backend_producer(self, uri, custom_producer):
        server_factory = self._crosscheck_ws_server_uri(listen=uri.geturl(), legacy=True)
        if not server_factory:
            twisted_producer = self._wsl_twisted_producer_type(
                custom_producer=custom_producer
            )
            server_factory = self._websocket.LegacyBroadcastServerFactory(
                uri.geturl()
            )
            server_factory.protocol = self._websocket.LegacyBroadcastServerProtocol
            server_factory.registerProducer(twisted_producer, streaming=True)
            self._wsl_twisted_servers[uri.geturl()] = server_factory
            server_factory.listen()

        return server_factory.producer

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


backend_by_type = {
    'twisted': TwistedBackend,
    'dummy': DummyBackend
}


def get_backend(backend_name):
    try:
        return backend_by_type.get(backend_name)
    except KeyError:
        raise ConfigurationError(
            ERR_NO_SUCH_COMPONENT.format(
                type_name=backend_name
            )
        )


class UniversalBackend(RequiredConfig):
    required_config = Namespace()
    required_config.backend = backend = Namespace()
    backend.add_option('type', default='twisted', from_string_converter=get_backend)
