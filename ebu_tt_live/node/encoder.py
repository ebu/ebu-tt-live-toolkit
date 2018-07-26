import logging
from datetime import timedelta, datetime
from .base import AbstractCombinedNode
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.documents.converters import EBUTT3EBUTTDConverter
from ebu_tt_live.documents import EBUTTDDocument, EBUTT3Document
from ebu_tt_live.bindings import d_style_type
from ebu_tt_live.config.clocks import get_date
import requests


log = logging.getLogger(__name__)


class EBUTTDEncoder(AbstractCombinedNode):

    _ebuttd_converter = None
    _default_ns = None
    _default_ebuttd_doc = None
    _expects = EBUTT3Document
    _provides = EBUTTDDocument
    # _begin_count is used to override the first output document count number. when
    # provided as a constructor value it is stored, and set on the output carriage
    # impl once before the first time emit_document is called. Then it is reset
    # to None, which is used as the test to see if it needs to be used.
    _begin_count = None

    def __init__(self, node_id, media_time_zero, default_ns=False, producer_carriage=None,
                 consumer_carriage=None, begin_count=None, clock_url=None, **kwargs):
        super(EBUTTDEncoder, self).__init__(
            producer_carriage=producer_carriage,
            consumer_carriage=consumer_carriage,
            node_id=node_id,
            **kwargs
        )
        self._default_ns = default_ns
        media_clock = MediaClock()
        if clock_url is None:
            media_clock.adjust_time(timedelta(), media_time_zero)
        else:
            log.info('Getting time from {}'.format(clock_url))
            r = requests.get(clock_url).text
            log.info('Got response {}'.format(r))
            d = get_date(r)
            t = d - datetime.min
            media_clock.adjust_time(t, media_time_zero)
        self._begin_count = begin_count
        self._ebuttd_converter = EBUTT3EBUTTDConverter(
            media_clock=media_clock
        )
        self._default_ebuttd_doc = EBUTTDDocument(lang='en-GB')
        self._default_ebuttd_doc.set_implicit_ns(self._default_ns)
        self._default_ebuttd_doc.validate()

    def process_document(self, document, **kwargs):
        # Convert each received document into EBU-TT-D
        if self.is_document(document):
            self.limit_sequence_to_one(document)


            converted_doc = EBUTTDDocument.create_from_raw_binding(
                self._ebuttd_converter.convert_document(document.binding)
            )
            
            body_style = d_style_type(id='bodyStyle', 
                                      fillLineGap='true', 
                                      fontFamily='reith Sans,proportionalSansSerif',
                                      fontSize = '160%',
                                      linePadding = '0.5c')
            self._ebuttd_converter.add_body_style(converted_doc._ebuttd_content, body_style)
            
            # If this is the first time, and there's a begin count override, apply it
            if self._begin_count is not None:
                # Will fail unless the concrete producer carriage impl is a FilesystemProducerImpl
                self.producer_carriage.producer_carriage.set_message_counter(self._begin_count)
                self._begin_count = None

            # Specify the time_base since the FilesystemProducerImpl can't derive it otherwise.
            # Hard coded to 'media' because that's all that's permitted in EBU-TT-D. Alternative
            # would be to extract it from the EBUTTDDocument but since it's the only permitted
            # value that would be an unnecessary overhead...
            self.producer_carriage.emit_data(data=converted_doc, sequence_identifier='default', time_base='media', **kwargs)
