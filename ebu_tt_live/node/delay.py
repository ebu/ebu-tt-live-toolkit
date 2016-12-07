
from .base import Node
from datetime import timedelta
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType, FullClockTimingType


class RetimingDelayNode(Node):

    _reference_clock = None
    _document_sequence = None
    _fixed_delay = None

    def __init__(self, node_id, carriage_impl, reference_clock, fixed_delay, document_sequence):
        super(RetimingDelayNode, self).__init__(node_id, carriage_impl)
        self._reference_clock = reference_clock
        self._fixed_delay = fixed_delay
        self._document_sequence = document_sequence

    def process_document(self, document):

        # change the sequence identifier
        document.sequence_identifier = self._document_sequence

        # TODO: add an ebuttm:appliedProcessing element to the document metadata

        if is_explicitly_timed(document.binding):

            # the document is explicitly timed, we propagate the modification on all elements
            update_children_timing(document.binding, document.time_base, self._fixed_delay)

        else:

            # the document is implicitly timed, we only modify the body timing
            update_body_timing(document.binding.body, document.time_base, self._fixed_delay)

        document.validate()
        self._carriage_impl.emit_document(document)


class BufferDelayNode(Node):

    _reference_clock = None
    _document_sequence = None
    _fixed_delay = None

    def __init__(self, node_id, carriage_impl, reference_clock, fixed_delay, document_sequence):
        super(BufferDelayNode, self).__init__(node_id, carriage_impl)
        self._reference_clock = reference_clock
        self._fixed_delay = fixed_delay
        self._document_sequence = document_sequence

    def process_document(self, document):

        self._carriage_impl.emit_document(document, delay=self._fixed_delay)


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

            if hasattr(child.value, 'begin') and child.value.begin != None:

                if timebase == 'clock':
                    delay = LimitedClockTimingType(timedelta(seconds=delay_int))
                    child.value.begin = LimitedClockTimingType(child.value.begin.timedelta + delay.timedelta)
                elif timebase == 'media':
                    delay = FullClockTimingType(timedelta(seconds=delay_int))
                    child.value.begin = FullClockTimingType(child.value.begin.timedelta + delay.timedelta)

            else:
                update_children_timing(child.value, timebase, delay_int)


def update_body_timing(body, timebase, delay_int):

    if timebase == 'clock':
        delay = LimitedClockTimingType(timedelta(seconds=delay_int))
        body.begin = LimitedClockTimingType(delay.timedelta)

    elif timebase == 'media':
        delay = FullClockTimingType(timedelta(seconds=delay_int))
        body.begin = FullClockTimingType(delay.timedelta)


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
