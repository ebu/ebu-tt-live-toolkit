
from ebu_tt_live.node import ProducerNode
from twisted.internet import interfaces
from zope.interface import implementer
import logging


log = logging.getLogger(__name__)


class TwistedProducerMixin(ProducerNode):

    _twisted_producer = None

    def register_twisted_producer(self, producer):
        self._twisted_producer = producer

    def emit_document(self, document):
        self._twisted_producer.emit_data(document.sequence_identifier, document.get_xml())


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
        self._custom_producer.process_document(None)

    def stopProducing(self):
        pass
