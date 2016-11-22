from .common import ConfigurableComponent, Namespace
from ebu_tt_live.carriage.twisted import TwistedProducerImpl, TwistedConsumerImpl
from ebu_tt_live.twisted import websocket


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

    @classmethod
    def configure(cls, config, local_config):
        out_carriage = TwistedProducerImpl()
        out_carriage.twisted_channel = local_config.channel

        factory = websocket.BroadcastServerFactory(local_config.uri)
        factory.protocol = websocket.StreamingServerProtocol
        factory.listen()


class WebsocketInput(WebsocketBase):
    pass


