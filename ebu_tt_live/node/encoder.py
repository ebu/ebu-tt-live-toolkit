from datetime import timedelta
from .base import AbstractCombinedNode
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.documents.converters import EBUTT3EBUTTDConverter
from ebu_tt_live.documents import EBUTTDDocument, EBUTT3Document
import logging

log = logging.getLogger(__name__)


class EBUTTDEncoder(AbstractCombinedNode):

    _ebuttd_converter = None
    _default_ns = None
    _default_ebuttd_doc = None
    _expects = EBUTT3Document
    _provides = EBUTTDDocument

    def __init__(self,
                 node_id,
                 media_time_zero,
                 default_ns=False,
                 calculate_active_area=False,
                 producer_carriage=None,
                 consumer_carriage=None,
                 **kwargs):
        super(EBUTTDEncoder, self).__init__(
            producer_carriage=producer_carriage,
            consumer_carriage=consumer_carriage,
            node_id=node_id,
            **kwargs
        )
        self._default_ns = default_ns
        media_clock = MediaClock()
        media_clock.adjust_time(timedelta(), media_time_zero)
        self._ebuttd_converter = EBUTT3EBUTTDConverter(
            media_clock=media_clock,
            calculate_active_area=calculate_active_area
        )
        self._default_ebuttd_doc = EBUTTDDocument(lang='en-GB')
        self._default_ebuttd_doc.implicit_ns = self._default_ns
        self._default_ebuttd_doc.validate()

    def process_document(self, document, **kwargs):
        # Convert each received document into EBU-TT-D
        if self.is_document(document):

            if self.check_if_document_seen(document=document):

                self.limit_sequence_to_one(document)

                # Convert the document
                converted_doc = self.convert_document(document)

                # Specify the time_base since the FilesystemProducerImpl can't
                # derive it otherwise.
                # Hard coded to 'media' because that's all that's permitted in
                # EBU-TT-D. Alternative would be to extract it
                # from the EBUTTDDocument but since it's the only permitted
                # value that would be an unnecessary overhead...
                self.producer_carriage.emit_data(
                    data=converted_doc,
                    sequence_identifier='default',
                    time_base='media',
                    **kwargs)
            else:
                log.warning(
                    'Ignoring duplicate document: {}__{}'.format(
                        document.sequence_identifier,
                        document.sequence_number
                    )
                )
        else:
            log.warning(
                'Ignoring incoming data that is not a document'
            )

    def convert_document(self, document):
        document.validate()
        doc = EBUTTDDocument.create_from_raw_binding(
            self._ebuttd_converter.convert_document(document.binding)
        )
        doc.implicit_ns = self._default_ebuttd_doc.implicit_ns
        if doc.binding.lang is None:
            doc.lang.binding = self._default_ebuttd_doc.binding.lang

        return doc
