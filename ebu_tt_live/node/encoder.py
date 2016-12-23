
from datetime import timedelta
from .base import AbstractCombinedNode
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.documents.converters import EBUTT3EBUTTDConverter
from ebu_tt_live.documents import EBUTTDDocument, EBUTT3Document


class EBUTTDEncoder(AbstractCombinedNode):

    _ebuttd_converter = None
    _default_ns = None
    _default_ebuttd_doc = None
    _expects = EBUTT3Document
    _provides = EBUTTDDocument

    def __init__(self, node_id, media_time_zero, default_ns=False, producer_carriage=None,
                 consumer_carriage=None, **kwargs):
        super(EBUTTDEncoder, self).__init__(
            producer_carriage=producer_carriage,
            consumer_carriage=consumer_carriage,
            node_id=node_id
        )
        self._default_ns = default_ns
        media_clock = MediaClock()
        media_clock.adjust_time(timedelta(), media_time_zero)
        self._ebuttd_converter = EBUTT3EBUTTDConverter(
            media_clock=media_clock
        )
        self._default_ebuttd_doc = EBUTTDDocument(lang='en-GB')
        self._default_ebuttd_doc.set_implicit_ns(self._default_ns)
        self._default_ebuttd_doc.validate()

    def process_document(self, document, **kwargs):
        # Convert each received document into EBU-TT-D
        converted_doc = EBUTTDDocument.create_from_raw_binding(
            self._ebuttd_converter.convert_document(document.binding)
        )
        self.producer_carriage.emit_data(converted_doc, sequence_identifier='default', **kwargs)
