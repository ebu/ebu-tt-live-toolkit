
from .base import Node
from ebu_tt_live.documents import EBUTT3DocumentSequence
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
        log.info(document.get_xml())

    @property
    def reference_clock(self):
        return self._reference_clock

    @reference_clock.setter
    def reference_clock(self, value):
        self._reference_clock = value
