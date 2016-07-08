
from ebu_tt_live.node import ProducerCarriageImpl, ConsumerCarriageImpl
from twisted.internet import interfaces
from zope.interface import implementer
from ebu_tt_live.bindings import CreateFromDocument
from ebu_tt_live.strings import ERR_DECODING_XML_FAILED
from ebu_tt_live.errors import XMLParsingFailed
from ebu_tt_live.documents import EBUTT3Document
import logging
import os


log = logging.getLogger(__name__)


class TwistedFileSystemProducerImpl(ProducerCarriageImpl):

    _manifest_path = None
    _dirpath = None
    _manifest_file = None

    def __init__(self, dirpath):
        self._dirpath = dirpath
        if not os.path.exists(self._dirpath):
            os.makedirs(self._dirpath)
        self._manifest_path = os.path.join(dirpath, 'manifest.txt')
        self._manifest_file = open(self._manifest_path, 'w')

    def resume_producing(self):
        # None, since this is a producer module. It will produce a new document.
        while self._node.process_document(document=None):
            pass
        self._manifest_file.close()

    def emit_document(self, document):
        filename = '{}_{}.xml'.format(document.sequence_identifier, document.sequence_number)
        filepath = os.path.join(self._dirpath, filename)
        with open(filepath, 'w') as f:
            f.write(document.get_xml())
        self._manifest_file.write('{},{}\n'.format(self._node.reference_clock.get_time(), filename))


class TwistedProducerImpl(ProducerCarriageImpl):

    _twisted_producer = None

    def register_twisted_producer(self, producer):
        self._twisted_producer = producer

    def resume_producing(self):
        # None, since this is a producer module. It will produce a new document.
        self._node.process_document(document=None)

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
        self._custom_producer.resume_producing()

    def stopProducing(self):
        pass


class TwistedConsumerImpl(ConsumerCarriageImpl):

    def on_new_data(self, data):
        document = None
        try:
            document = EBUTT3Document.create_from_raw_binding(CreateFromDocument(data))
        except:
            log.exception(ERR_DECODING_XML_FAILED)
            raise XMLParsingFailed(ERR_DECODING_XML_FAILED)

        if document:
            self._node.process_document(document)


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
