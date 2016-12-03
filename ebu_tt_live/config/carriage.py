from .common import ConfigurableComponent, Namespace
from ebu_tt_live.carriage.direct import DirectCarriageImpl
from ebu_tt_live.carriage.websocket import WebsocketProducerCarriage, WebsocketConsumerCarriage
import urlparse


def producer_carriage_by_type(carriage_type):
    if carriage_type == 'websocket':
        return WebsocketOutput
    elif carriage_type == 'filesystem':
        return FileOutput
    elif carriage_type == 'direct':
        return DirectOutput
    else:
        raise Exception('No such component: {}'.format(carriage_type))


def consumer_carriage_by_type(carriage_type):
    if carriage_type == 'websocket':
        return WebsocketInput
    elif carriage_type == 'direct':
        return DirectInput
    else:
        raise Exception('No such component: {}'.format(carriage_type))


class DirectCommon(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('id', default='default')

    _components = {}

    def __init__(self, config, local_config, **kwargs):
        super(DirectCommon, self).__init__(
            config=config,
            local_config=local_config,
            **kwargs
        )
        self.backend.register_component_start(self)

    @classmethod
    def configure_component(cls, config, local_config, **kwargs):
        instance = cls(config=config, local_config=local_config)
        component = cls._components.get(local_config.id, None)

        if component is None:
            instance.component = DirectCarriageImpl()
            cls._components[local_config.id] = instance.component
        else:
            instance.component = component

        return instance


class DirectInput(DirectCommon):
    pass


class DirectOutput(DirectCommon):

    _looping_call = None

    def start(self):
        # At the moment this is twisted specific... investigate other options.
        from ebu_tt_live.twisted import task

        self._looping_call = task.LoopingCall(self.component.resume_producing)
        self._looping_call.start(2.0, now=False)


# File-based carriage mechanism configurators
# ===========================================
class FileOutput(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('folder', default='./export')


# Websocket carriage mechanism configurators
# ==========================================


def str_to_url_converter(value):
    parsed = urlparse.urlparse(value)
    return parsed



class WebsocketBase(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('uri', default='ws://localhost:9001', from_string_converter=str_to_url_converter)


class WebsocketOutput(WebsocketBase):

    _backend_producer = None
    _looping_call = None

    def __init__(self, config, local_config):
        super(WebsocketOutput, self).__init__(config, local_config)
        self.component = WebsocketProducerCarriage()
        self.backend.register_component_start(self)

    def start(self):
        self._backend_producer = self.backend.ws_backend_producer(uri=self.config.uri, custom_producer=self.component)


class WebsocketInput(WebsocketBase):

    _backend_consumer = None

    def __init__(self, config, local_config):
        super(WebsocketInput, self).__init__(config, local_config)
        self.component = WebsocketConsumerCarriage()
        self.backend.register_component_start(self)

    def start(self):
        self._backend_consumer = self.backend.ws_backend_consumer(uri=self.config.uri, custom_consumer=self.component)
