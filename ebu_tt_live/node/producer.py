import logging
from .base import AbstractProducerNode
from datetime import timedelta
from ebu_tt_live.bindings import div_type, br_type, p_type, style_type, \
    styling, layout, region_type, span_type
from ebu_tt_live.bindings._ebuttm import pMetadata_type, divMetadata_type
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.errors import EndOfData
from ebu_tt_live.strings import END_OF_DATA, DOC_PRODUCED

document_logger = logging.getLogger('document_logger')


class SimpleProducer(AbstractProducerNode):

    _document_sequence = None
    _input_blocks = None
    _reference_clock = None
    _provides = EBUTT3Document

    def __init__(
            self, node_id, producer_carriage, document_sequence, input_blocks):
        super(SimpleProducer, self).__init__(
            node_id=node_id, producer_carriage=producer_carriage)
        self._document_sequence = document_sequence
        self._input_blocks = input_blocks
        self._reference_clock = document_sequence.reference_clock

    @property
    def reference_clock(self):
        return self._reference_clock

    @property
    def document_sequence(self):
        return self._document_sequence

    @staticmethod
    def _interleave_line_breaks(items, style=None):
        # Create a metadata child element. Note that this method works
        # and does not generate an exception, whereas the commented out
        # method in process_document() below does not work. 
        end_list = [
            pMetadata_type(
                desc='pMetadata_type test'
            )
        ]
        for item in items:
            end_list.append(
                span_type(
                    item,
                    style=style,
                    _strict_keywords=False
                )
            )
            end_list.append(br_type())
        # We don't require the last linebreak so remove it.
        end_list.pop()
        return end_list

    def _create_fragment(self, lines, style=None):
        return div_type(
            p_type(
                *self._interleave_line_breaks(lines, style=style),
                id='ID{:03d}'.format(1),
                _strict_keywords=False
            ),
            region='bottomRegion'
        )

    def process_document(self, document=None, **kwargs):

        activation_time = \
            self._reference_clock.get_time() \
            + timedelta(seconds=1)

        if self._input_blocks:
            try:
                lines = next(self._input_blocks)
            except StopIteration:
                raise EndOfData(END_OF_DATA)
        else:
            lines = [LimitedClockTimingType(activation_time)]

        document = self._document_sequence.new_document()

        # Add default style
        document.binding.head.styling = styling(
            style_type(
                id='defaultStyle1',
                backgroundColor="rgb(0, 0, 0)",
                color="rgb(255, 255, 255)",
                linePadding="0.5c",
                fontFamily="sansSerif"
            )
        )
        document.binding.head.layout = layout(
            region_type(
                id='bottomRegion',
                origin='14.375% 60%',
                extent='71.25% 24%',
                displayAlign='after',
                writingMode='lrtb',
                overflow="visible"
            )
        )
        document.add_div(
            self._create_fragment(
                lines,
                'defaultStyle1'
            ),
        )

        for div in document.binding.body.div:
            div.metadata = divMetadata_type(desc='divMetadata_type test')
            # The following commented out code causes an exception downstream,
            # but it is not obvious why. Leaving it here for posterity, in case
            # a fix is ever found.
            # The exception is a
            # pyxb.exceptions_.UnprocessedElementContentError
            # for p in div.p:
            #     p.metadata = pMetadata_type(desc='pMetadata_type test')

        document.set_dur(LimitedClockTimingType(timedelta(seconds=1)))
        document.set_begin(LimitedClockTimingType(activation_time))

        document.validate()

        document_logger.info(
            DOC_PRODUCED.format(
                sequence_identifier=document.sequence_identifier,
                sequence_number=document.sequence_number
            )
        )
        self.producer_carriage.emit_data(document, **kwargs)
