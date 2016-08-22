from datetime import timedelta

from ebu_tt_live.bindings.ebutt_live._ebuttdt import LimitedClockTimingType
from ebu_tt_live.bindings.ebutt_live import div_type, br_type, p_type
from ebu_tt_live.errors import EndOfData
from ebu_tt_live.strings import END_OF_DATA

from .base import Node


class SimpleProducer(Node):

    _document_sequence = None
    _input_blocks = None
    _reference_clock = None

    def __init__(self, node_id, carriage_impl, document_sequence, input_blocks):
        super(SimpleProducer, self).__init__(node_id, carriage_impl)
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
    def _interleave_line_breaks(items):
        end_list = []
        for item in items:
            end_list.append(item)
            end_list.append(br_type())
        # We don't require the last linebreak so remove it.
        end_list.pop()
        return end_list

    def _create_fragment(self, lines):
        return div_type(
            p_type(
                *self._interleave_line_breaks(lines),
                id='ID{:03d}'.format(1)
            )
        )

    def process_document(self, document):

        activation_time = self._reference_clock.get_time() + timedelta(seconds=1)

        if self._input_blocks:
            try:
                lines = self._input_blocks.next()
            except StopIteration:
                raise EndOfData(END_OF_DATA)
        else:
            lines = [LimitedClockTimingType(activation_time)]

        document = self._document_sequence.new_document()

        document.add_div(
            self._create_fragment(
                lines
            )
        )

        document.set_dur(LimitedClockTimingType(timedelta(seconds=1)))
        document.set_begin(LimitedClockTimingType(activation_time))

        document.validate()

        self._carriage_impl.emit_document(document)
