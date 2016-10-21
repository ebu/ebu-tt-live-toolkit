
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
        if is_explicitly_timed(document.binding):

            update_children_timing(document.binding, document.time_base, fixed_delay_int)
            self._carriage_impl.emit_document(document)

        # document is implicitly timed: pause a while, re-emit later
        else:

            time.sleep(fixed_delay_int)
            self._carriage_impl.emit_document(document)


def update_children_timing(element, timebase, delay_int):

    # if the element has a child
    if hasattr(element, 'orderedContent'):

        children = element.orderedContent()

        for child in children:

            if hasattr(child.value, 'end') and child.value.end != None:

                if timebase == 'clock':
                    delay = LimitedClockTimingType(timedelta(seconds=delay_int))
                    child.value.end = LimitedClockTimingType(child.value.end.timedelta + delay.timedelta)
                elif timebase == 'media':
                    delay = FullClockTimingType(timedelta(seconds=delay_int))
                    child.value.end = FullClockTimingType(child.value.end.timedelta + delay.timedelta)
                    # TODO: smpte

            if hasattr(child.value, 'begin') and child.value.begin != None:

                if timebase == 'clock':
                    delay = LimitedClockTimingType(timedelta(seconds=delay_int))
                    child.value.begin = LimitedClockTimingType(child.value.begin.timedelta + delay.timedelta)
                elif timebase == 'media':
                    delay = FullClockTimingType(timedelta(seconds=delay_int))
                    child.value.begin = FullClockTimingType(child.value.begin.timedelta + delay.timedelta)
                # TODO: permit timebase = "smpte" with clockMode="continuous"

            else:
                update_children_timing(child.value, timebase, delay_int)


def is_explicitly_timed(element):

    # if element has begin or end attribute
    if hasattr(element, 'begin') and element.begin != None or hasattr(element, 'end') and element.end != None:
        return True

    else:

        # if element has children
        if hasattr(element, 'orderedContent'):

            children = element.orderedContent()

            for child in children:
                res = is_explicitly_timed(child.value)
                if res:
                    return res
