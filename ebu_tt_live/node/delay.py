
from .base import Node
from datetime import timedelta
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType, FullClockTimingType
import time
import random


class FixedDelayNode(Node):

    _reference_clock = None
    _sequence = None

    def __init__(self, node_id, carriage_impl, reference_clock):
        super(FixedDelayNode, self).__init__(node_id, carriage_impl)
        self._reference_clock = reference_clock

        random_int = random.randint(0, 9999999999)
        new_identifier = 'sequence_{0}'.format(str(random_int))
        self._sequence = new_identifier

    def process_document(self, document):

        fixed_delay = LimitedClockTimingType(timedelta(seconds=2))

        # change the sequence identifier
        document.sequence_identifier = self._sequence

        # TODO: add an ebuttm:trace element to the document metadata

        # document is explicitly timed: modify the document
        if document.binding.body.begin or document.binding.body.end:

            if document.time_base == 'clock':

                document.set_begin(
                    LimitedClockTimingType(document.binding.body.begin.timedelta + fixed_delay.timedelta))

                document.set_end(
                    LimitedClockTimingType(document.binding.body.begin.timedelta + fixed_delay.timedelta))

                document.set_dur(
                    LimitedClockTimingType(document.binding.body.begin.timedelta + fixed_delay.timedelta))

            elif document.time_base == 'media':

                document.set_begin(
                    FullClockTimingType(document.binding.body.begin.timedelta + fixed_delay.timedelta))

                document.set_end(
                    FullClockTimingType(document.binding.body.begin.timedelta + fixed_delay.timedelta))

                document.set_dur(
                    FullClockTimingType(document.binding.body.begin.timedelta + fixed_delay.timedelta))

            # TODO: traverse all the elements on content and change their begin/end/dur attributes

            self._carriage_impl.emit_document(document)

        # document is implicitly timed: pause a while, re-emit later
        else:

            time.sleep(fixed_delay)
            self._carriage_impl.emit_document(document)
