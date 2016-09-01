
from .base import Node
from ebu_tt_live.documents import EBUTT3DocumentSequence, ebutt3_to_ebuttd
from ebu_tt_live.strings import DOC_RECEIVED
from datetime import timedelta
import logging


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class SimpleConsumer(Node):

    _reference_clock = None
    _sequence = None

    def __init__(self, node_id, carriage_impl, reference_clock):
        super(SimpleConsumer, self).__init__(node_id, carriage_impl)
        self._reference_clock = reference_clock

    def process_document(self, document):
        if self._sequence is None:
            # Create sequence from document
            log.info('Creating document sequence from first document {}'.format(
                document
            ))
            self._sequence = EBUTT3DocumentSequence.create_from_document(document)
            self._reference_clock = self._sequence.reference_clock
            if document.availability_time is None:
                document.availability_time = self._reference_clock.get_time()

        document_logger.info(DOC_RECEIVED.format(
            sequence_number=document.sequence_number,
            sequence_identifier=document.sequence_identifier,
            computed_begin_time=document.computed_begin_time,
            computed_end_time=document.computed_end_time
        ))
        self._sequence.add_document(document)

    @property
    def reference_clock(self):
        return self._reference_clock

    @reference_clock.setter
    def reference_clock(self, value):
        self._reference_clock = value


class EBUTTDConverterConsumer(SimpleConsumer):

    def process_document(self, document):
        super(EBUTTDConverterConsumer, self).process_document(document)
        # segmentation, conversion... here

    def convert_to_ebuttd(self, begin=None, end=None):
        if self._sequence is not None:
            segment_doc = self._sequence.extract_segment(begin=begin, end=end)
            return ebutt3_to_ebuttd(segment_doc)
        return None

    def convert_next_segment(self):
        # Figure out begin and end
        ebuttd_doc = self.convert_to_ebuttd(begin=None, end=None)
        if ebuttd_doc is not None:
            log.info(ebuttd_doc.get_xml())

