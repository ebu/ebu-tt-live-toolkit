
from twisted.internet import interfaces, reactor
from zope.interface import implementer
import logging


log = logging.getLogger(__name__)


@implementer(interfaces.IPushProducer)
class TwistedPushProducer(object):
    """
    This is a Twisted Push producer. The concept is related to twisted and it is not the same as our producer
    and consumer nodes.
    """

    _custom_producer = None
    _consumer = None

    def __init__(self, consumer, custom_producer):
        self._custom_producer = custom_producer
        self._consumer = consumer
        self._consumer.registerProducer(self, False)
        self._custom_producer.register_backend_producer(self)

    def emit_data(self, sequence_identifier, data, delay=None):
        if delay is not None:
            reactor.callLater(delay, self._consumer.write, sequence_identifier, data)
        else:
            self._consumer.write(sequence_identifier, data)

    def resumeProducing(self):
        self._custom_producer.resume_producing()

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


@implementer(interfaces.IConsumer)
class TwistedConsumer(object):
    """
    This is a Twisted Consumer producer. The concept is related to twisted and it is not the same as our producer
    and consumer nodes.
    """
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
