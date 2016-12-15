
from .base import AbstractConsumerNode, AbstractProducerNode, AbstractCombinedNode
from ebu_tt_live.documents import EBUTT3DocumentSequence, EBUTTDDocument, EBUTT3Document
from ebu_tt_live.documents.converters import EBUTT3EBUTTDConverter
from ebu_tt_live.strings import DOC_RECEIVED
from ebu_tt_live.clocks.media import MediaClock
from datetime import timedelta
import logging


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class SimpleConsumer(AbstractConsumerNode):

    _reference_clock = None
    _sequence = None
    _expects = EBUTT3Document

    def __init__(self, node_id, consumer_carriage=None, reference_clock=None, **kwargs):
        super(SimpleConsumer, self).__init__(
            node_id=node_id,
            consumer_carriage=consumer_carriage
        )
        self._reference_clock = reference_clock

    def process_document(self, document, **kwargs):
        if self._sequence is None:
            # Create sequence from document
            log.info('Creating document sequence from first document {}'.format(
                document
            ))
            self._sequence = EBUTT3DocumentSequence.create_from_document(document)
            if self._reference_clock is None:
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


class EBUTTDEncoderNode(AbstractCombinedNode):

    _ebuttd_converter = None
    _default_ebuttd_doc = None
    _implicit_ns = False
    _expects = EBUTT3Document
    _provides = EBUTTDDocument

    def __init__(self, node_id, producer_carriage=None, consumer_carriage=None, **kwargs):
        super(EBUTTDEncoderNode, self).__init__(
            node_id=node_id,
            producer_carriage=producer_carriage,
            consumer_carriage=consumer_carriage,
            **kwargs
        )

    def process_document(self, document, **kwargs):
        pass


class ReSequencer(AbstractProducerNode, SimpleConsumer):

    _last_segment_end = None
    _segment_length = None
    _outbound_carriage_impl = None
    _segment_timer = None
    _discard = None
    _expects = EBUTT3Document
    _provides = EBUTT3Document

    def __init__(self, node_id, reference_clock, segment_length, media_time_zero, segment_timer, discard,
                 segmentation_starts=None, implicit_ns=False, consumer_carriage=None,
                 producer_carriage=None, **kwargs):
        super(ReSequencer, self).__init__(
            node_id=node_id,
            consumer_carriage=consumer_carriage,
            producer_carriage=producer_carriage,
            reference_clock=reference_clock,
            **kwargs
        )
        # We need clock factory to figure the timesync out
        self._last_segment_end = reference_clock.get_time()
        self._segment_length = timedelta(seconds=segment_length)
        media_clock = MediaClock()
        media_clock.adjust_time(timedelta(), media_time_zero)
        self._ebuttd_converter = EBUTT3EBUTTDConverter(
            media_clock=media_clock
        )
        self._implicit_ns = implicit_ns
        # Setting this globally so we don't have to do it everywhere
        EBUTTDDocument._implicit_ns = self._implicit_ns
        self._default_ebuttd_doc = EBUTTDDocument(lang='en-GB')
        self._default_ebuttd_doc.validate()
        self._segment_timer = segment_timer
        self._discard = discard
        if segmentation_starts is not None:
            self._last_segment_end = segmentation_starts

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
        # segmentation here
        if sequence_missing and self._sequence is not None:
            # Ok we just got a relevant document. Let's call the function
            # that schedules the periodic segmentation.
            self._segment_timer = self._segment_timer(self)

    def get_segment(self, begin=None, end=None):
        if self._sequence is not None:
            segment_doc = self._sequence.extract_segment(begin=begin, end=end, discard=self._discard)
            return segment_doc
        return None

    def convert_next_segment(self):
        # Figure out begin and end
        ebutt3_doc = self.get_segment(
            begin=self.last_segment_end,
            end=self.last_segment_end + self._segment_length
        )
        if ebutt3_doc is not None:
            ebuttd_bindings = self._ebuttd_converter.convert_document(ebutt3_doc.binding)
            ebuttd_doc = EBUTTDDocument.create_from_raw_binding(ebuttd_bindings)
            ebuttd_doc.validate()
        else:
            ebuttd_doc = self._default_ebuttd_doc
        self.increment_last_segment_end(self._segment_length)
        self._outbound_carriage_impl.emit_data(ebuttd_doc)
        return self.last_segment_end
