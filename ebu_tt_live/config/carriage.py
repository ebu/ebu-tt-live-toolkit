from .common import ConfigurableComponent, Namespace
from ebu_tt_live.carriage.twisted import TwistedProducerImpl, TwistedConsumerImpl


def carriage_by_type(carriage_type):
    if carriage_type == 'websocket-input':
        return WebsocketInput
    elif carriage_type == 'websocket-output':
        return WebsocketOutput
    else:
        raise Exception('No such component: {}'.format(carriage_type))


# File-based carriage mechanism configurators
# ===========================================
class FileOutput(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('folder', default='./export')


# Websocket carriage mechanism configurators
# ==========================================
class WebsocketBase(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('uri', default='ws://localhost:9001')
    required_config.add_option('channel', default='TestSequence1')


class WebsocketOutput(WebsocketBase):

    _pull_producer = None
    _looping_call = None

    def __init__(self, config, local_config):
        super(WebsocketOutput, self).__init__(config, local_config)
        self.component = TwistedProducerImpl()
        self.component.twisted_channel = local_config.channel

    def start(self):
        from ebu_tt_live.twisted import websocket, TwistedPullProducer, task

        factory = websocket.BroadcastServerFactory(self.config.uri)
        factory.protocol = websocket.StreamingServerProtocol

        self._pull_producer = TwistedPullProducer(
            consumer=factory,
            custom_producer=self.component
        )

        self._looping_call = task.LoopingCall(factory.pull)

        self._looping_call.start(2.0)
        factory.listen()


class WebsocketInput(WebsocketBase):
    pass


