
import six
from .base import AbstractCombinedNode
from datetime import timedelta
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType, FullClockTimingType
from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings.pyxb_utils import RecursiveOperation, StopBranchIteration
from ebu_tt_live.bindings.validation.timing import TimingValidationMixin


class RetimingDelayNode(AbstractCombinedNode):

    _reference_clock = None
    _document_sequence = None
    _fixed_delay = None
    _expects = EBUTT3Document
    _provides = EBUTT3Document

    def __init__(self, node_id, carriage_impl, reference_clock, fixed_delay, document_sequence):
        super(RetimingDelayNode, self).__init__(
            node_id=node_id,
            producer_carriage=carriage_impl
        )
        self._reference_clock = reference_clock
        self._fixed_delay = fixed_delay
        self._document_sequence = document_sequence

    def process_document(self, document, **kwargs):

        # change the sequence identifier
        document.sequence_identifier = self._document_sequence

        # TODO: add an ebuttm:appliedProcessing element to the document metadata

        if has_a_leaf_with_no_timing_path(document.binding.body):
            update_body_timing(document.binding.body, document.time_base, self._fixed_delay)

        else:
            update_children_timing(document.binding, document.time_base, self._fixed_delay)

        document.validate()
        self.producer_carriage.emit_data(data=document, **kwargs)


class BufferDelayNode(AbstractCombinedNode):

    _fixed_delay = None
    _expects = six.text_type
    _provides = six.text_type

    def __init__(self, node_id, producer_carriage, fixed_delay):
        super(BufferDelayNode, self).__init__(
            node_id=node_id,
            producer_carriage=producer_carriage
        )
        self._fixed_delay = fixed_delay

    def process_document(self, document, **kwargs):

        self.producer_carriage.emit_data(data=document, delay=self._fixed_delay, **kwargs)


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

    if hasattr(body, 'begin'):
        assert body.begin == None, "The body already has a begin time"

    # we always update the begin attribute, regardless of the presence of a begin or end attribute
    if timebase == 'clock':
        delay = LimitedClockTimingType(timedelta(seconds=delay_int))
        body.begin = LimitedClockTimingType(delay.timedelta)

    elif timebase == 'media':
        delay = FullClockTimingType(timedelta(seconds=delay_int))
        body.begin = FullClockTimingType(delay.timedelta)

    # if the body has an end attribute, we add to it the value of the delay
    if hasattr(body, 'end') and body.end != None:

        if timebase == 'clock':
            delay = LimitedClockTimingType(timedelta(seconds=delay_int))
            body.end = LimitedClockTimingType(body.end.timedelta + delay.timedelta)

        elif timebase == 'media':
            delay = FullClockTimingType(timedelta(seconds=delay_int))
            body.end = FullClockTimingType(body.end.timedelta + delay.timedelta)


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


class UntimedPathFinder(RecursiveOperation):

    _path_found = False
    _timed_element_stack = None

    def __init__(self, root_element):
        self._timed_element_stack = []
        super(UntimedPathFinder, self).__init__(
            root_element,
            filter=lambda value, element: isinstance(value, TimingValidationMixin)
        )

    def _is_begin_timed(self, value):
        if value.begin is not None:
            return True
        else:
            return False

    def _before_element(self, value, element=None, parent_binding=None, **kwargs):
        if self._path_found is True:
            raise StopBranchIteration()
        if self._is_begin_timed(value=value):
            self._timed_element_stack.append(value)

    def _after_element(self, value, element=None, parent_binding=None, **kwargs):
        if self._is_begin_timed(value=value):
            bla = self._timed_element_stack.pop()

    def _process_element(self, value, element=None, parent_binding=None, **kwargs):
        if value.is_timed_leaf() and not len(self._timed_element_stack):
            self._path_found = True
            raise StopBranchIteration()

    def _process_non_element(self, value, non_element, parent_binding=None, **kwargs):
        pass

    @property
    def path_found(self):
        return self._path_found


def has_a_leaf_with_no_timing_path(element):
    """
    Check if a document has at least one leaf that has no ancestor that has begin time or has begin time itself.
    @param element:
    @return:
    """

    finder = UntimedPathFinder(element)
    finder.proceed()

    return finder.path_found
