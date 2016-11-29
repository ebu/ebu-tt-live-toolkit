
from .base import ProducerCarriageImpl, ConsumerCarriageImpl
from ebu_tt_live.bindings import CreateFromDocument, CreateFromDOM
from ebu_tt_live.strings import ERR_DECODING_XML_FAILED
from ebu_tt_live.errors import XMLParsingFailed
from ebu_tt_live.documents import EBUTT3Document

from twisted.internet import reactor

import logging
from xml.dom import minidom


log = logging.getLogger(__name__)


class TwistedProducerImpl(ProducerCarriageImpl):

    _twisted_producer = None

    def register_twisted_producer(self, producer):
        self._twisted_producer = producer

    def resume_producing(self):
        # None, since this is a producer module. It will produce a new document.
        self._node.process_document(document=None)

    def emit_document(self, document, delay=None, **kwargs):

        if delay:
            reactor.callLater(delay, self._twisted_producer.emit_data, document.sequence_identifier, document.get_xml())

        self._twisted_producer.emit_data(document.sequence_identifier, document.get_xml())


class TwistedConsumerImpl(ConsumerCarriageImpl):

    def on_new_data(self, data):
        document = None
        try:
            document = EBUTT3Document.create_from_raw_binding(CreateFromDocument(data))
        except:
            log.exception(ERR_DECODING_XML_FAILED)
            raise XMLParsingFailed(ERR_DECODING_XML_FAILED)

        if document:
            document.availability_time = self._node.reference_clock.get_time()
            self._node.process_document(document)
