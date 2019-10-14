
from .base import AbstractConsumerNode, AbstractProducerNode
from ebu_tt_live.documents import EBUTT3DocumentSequence, EBUTT3Document
from ebu_tt_live.strings import DOC_RECEIVED
from ebu_tt_live.errors import SequenceNumberCollisionError
from datetime import timedelta
import logging


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class SimpleConsumer(AbstractConsumerNode):

    _reference_clock = None
    _sequence = None
    _verbose = None
    _expects = EBUTT3Document

    def __init__(self, node_id, consumer_carriage=None, reference_clock=None, verbose=False, **kwargs):
        super(SimpleConsumer, self).__init__(
            node_id=node_id,
            consumer_carriage=consumer_carriage
        )
        self._reference_clock = reference_clock
        self._verbose = verbose

    def process_document(self, document, **kwargs):
        if self.is_document(document):
            self.limit_sequence_to_one(document)

            if self._sequence is None:
                # Create sequence from document
                log.info('Creating document sequence from first document {}'.format(
                    document
                ))
                self.create_sequence_from_document(document)
            if document.availability_time is None:
                document.availability_time = self._reference_clock.get_time()

            document_logger.info(DOC_RECEIVED.format(
                sequence_number=document.sequence_number,
                sequence_identifier=document.sequence_identifier,
                computed_begin_time=document.computed_begin_time,
                computed_end_time=document.computed_end_time
            ))
            try:
                self._sequence.add_document(document)
            except SequenceNumberCollisionError:
                log.info(
                    'Consumer ignoring duplicate seq number: {}'.format(
                        document.sequence_number
                    )
                )

    def create_sequence_from_document(self, document):
        self._sequence = EBUTT3DocumentSequence.create_from_document(document, verbose=self._verbose)
        if self._reference_clock is None:
            self._reference_clock = self._sequence.reference_clock

    @property
    def reference_clock(self):
        return self._reference_clock

    @reference_clock.setter
    def reference_clock(self, value):
        self._reference_clock = value


class ReSequencer(AbstractProducerNode, SimpleConsumer):

    _last_segment_end = None
    _segment_length = None
    _segment_timer = None
    _discard = None
    _segment_counter = None
    _sequence_identifier = None
    _expects = EBUTT3Document
    _provides = EBUTT3Document

    def __init__(self, node_id, reference_clock, segment_length, discard, sequence_identifier,
                 consumer_carriage=None, producer_carriage=None, init_document=None, **kwargs):
        super(ReSequencer, self).__init__(
            node_id=node_id,
            consumer_carriage=consumer_carriage,
            producer_carriage=producer_carriage,
            reference_clock=reference_clock,
            **kwargs
        )
        self._last_segment_end = reference_clock.get_time()
        self._segment_length = timedelta(seconds=segment_length)
        # self._segment_timer = segment_timer
        self._segment_counter = 1
        self._sequence_identifier = sequence_identifier
        self._discard = discard
        
        if init_document is not None:
            # Create sequence from init document, in order to immediately start document output
            log.info('Creating document sequence from init document {}'.format(
                init_document
            ))
            with open(init_document, 'r') as xml_file:
                xml_content = xml_file.read()
            xml_doc = EBUTT3Document.create_from_xml(xml_content)
            self.create_sequence_from_document(xml_doc)

    @property
    def last_segment_end(self):
        return self._last_segment_end

    @property
    def segment_length(self):
        return self._segment_length

    def increment_last_segment_end(self, increment_by):
        self._last_segment_end += increment_by
        return self._last_segment_end

    def process_document(self, document, **kwargs):
        sequence_missing = self._sequence is None
        super(ReSequencer, self).process_document(document)
        # TODO: re-enable this functionality or remove it.
        # if sequence_missing and self._sequence is not None:
        #     # Ok we just got a relevant document. Let's call the function
        #     # that schedules the periodic segmentation.
        #     self._segment_timer = self._segment_timer(self)

    def get_segment(self, begin=None, end=None):
        if self._sequence is not None:
            segment_doc = self._sequence.extract_segment(
                begin=begin,
                end=end,
                discard=self._discard,
                sequence_number=self._segment_counter
            )
            if segment_doc is not None:
                segment_doc.sequence_identifier = self._sequence_identifier
                self._segment_counter += 1
            return segment_doc
        return None

    def convert_next_segment(self):
        # Figure out begin and end
        ebutt3_doc = self.get_segment(
            begin=self.last_segment_end,
            end=self.last_segment_end + self._segment_length
        )
        if ebutt3_doc is not None:
            self.increment_last_segment_end(self._segment_length)
            self.producer_carriage.emit_data(ebutt3_doc)
