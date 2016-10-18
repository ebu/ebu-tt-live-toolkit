
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

        # change the sequence identifier
        document.sequence_identifier = self._sequence

        # TODO: add an ebuttm:trace element to the document metadata

        fixed_delay_int = 2

        # document is explicitly timed: modify the document
        if document.binding.body.begin or document.binding.body.end:

            if document.time_base == 'clock':

                fixed_delay = LimitedClockTimingType(timedelta(seconds=fixed_delay_int))

                document.set_begin(
                    LimitedClockTimingType(document.binding.body.begin.timedelta + fixed_delay.timedelta))

                document.set_end(
                    LimitedClockTimingType(document.binding.body.end.timedelta + fixed_delay.timedelta))

                update_children_timing(document.binding, fixed_delay)

            elif document.time_base == 'media':

                fixed_delay = FullClockTimingType(timedelta(seconds=fixed_delay_int))

                document.set_begin(
                    FullClockTimingType(document.binding.body.begin.timedelta + fixed_delay.timedelta))

                document.set_end(
                    FullClockTimingType(document.binding.body.end.timedelta + fixed_delay.timedelta))

                update_children_timing(document.binding, fixed_delay)

            self._carriage_impl.emit_document(document)

        # document is implicitly timed: pause a while, re-emit later
        else:

            time.sleep(fixed_delay_int)
            self._carriage_impl.emit_document(document)


def update_children_timing(element, delay):

    # if the element has a child
    if hasattr(element, 'orderedContent'):

        children = element.orderedContent()

        for child in children:

            if hasattr(child.value, 'begin') and child.value.begin != None:
                child.value.begin = LimitedClockTimingType(child.value.begin.timedelta + delay.timedelta)

            if hasattr(child.value, 'end') and child.value.end != None:
                child.value.end = LimitedClockTimingType(child.value.end.timedelta + delay.timedelta)

            update_children_timing(child.value, delay)
