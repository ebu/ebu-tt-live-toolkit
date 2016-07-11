
from twisted.internet import interfaces
from zope.interface import implementer
import logging


log = logging.getLogger(__name__)


@implementer(interfaces.IPullProducer)
class TwistedPullProducer(object):

    _custom_producer = None
    _consumer = None

    def __init__(self, consumer, custom_producer):
        self._custom_producer = custom_producer
        self._consumer = consumer
        self._consumer.registerProducer(self, False)
        self._custom_producer.register_twisted_producer(self)

    def emit_data(self, channel, data):
        self._consumer.write(channel, data)

    def resumeProducing(self):
        self._custom_producer.resume_producing()

    def stopProducing(self):
        pass


@implementer(interfaces.IConsumer)
class TwistedConsumer(object):

    _custom_consumer = None
    _producer = None

    def __init__(self, custom_consumer):
        self._custom_consumer = custom_consumer

    def registerProducer(self, producer, streaming):
        self._producer = producer
        if streaming:
            self._producer.resumeProducing()

    def unregisterProducer(self):
        self._producer.stopProducing()
        self._producer = None

    def write(self, data):
        self._custom_consumer.on_new_data(data)
