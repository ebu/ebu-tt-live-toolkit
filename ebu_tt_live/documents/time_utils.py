from sortedcontainers import sortedset
from sortedcontainers import sortedlist
from datetime import timedelta

class TimingEvent(object):
    """
    This class wraps a document and an associated resolved timing event into an object that can be placed
    on the timeline.
    """

    _element = None
    _when = None

    def __init__(self, element, when):
        self._element = element
        self.when = when

    @property
    def when(self):
        return self._when

    @when.setter
    def when(self, value):
        if not isinstance(value, timedelta):
            ValueError()
        self._when = value

    @property
    def element(self):
        return self._element


# R16
class TimingEventBegin(TimingEvent):
    """
    Element/document resolved begin time
    """

    def __init__(self, element):
        super(TimingEventBegin, self).__init__(element=element, when=element.computed_begin_time)

    def __repr__(self):
        return '<{}({}): {}>'.format(
            type(self),
            self.when,
            self.element
        )


# R17
class TimingEventEnd(TimingEvent):
    """
    Element/document resolved end time.
    """
    def __init__(self, element):
        super(TimingEventEnd, self).__init__(element=element, when=element.computed_end_time)

    def __repr__(self):
        return '<{}({}): {}>'.format(
            type(self),
            self.when,
            self.element
        )


class TimelineUtilMixin(object):
    """
    This mixin is responsible for managing the shared timeline functionality
    """

    # The timing events that mark the beginning and end of an element are kept on a timeline,
    # which iw a sorted list. IMPORTANT: Not sorted set as there are overlapping begins and ends.
    _timeline = None

    @property
    def timeline(self):
        if self._timeline is None:
            self._timeline = sortedlist.SortedListWithKey(key=lambda item: item.when)
        return self._timeline

    def reset_timeline(self):
        self._timeline = None

    def add_to_timeline(self, element):
        """
        The element gets added to the timeline so it would be easier to look up.
        :param element:
        :return:
        """
        if element.computed_begin_time is not None:
            self.timeline.add(TimingEventBegin(element=element))
        if element.computed_end_time is not None:
            self.timeline.add(TimingEventEnd(element=element))

    def locate_element_begin(self, element):
        for item in self.timeline.irange(TimingEventBegin(element)):
            if item.element == element and isinstance(item, TimingEventBegin):
                return item
        raise LookupError()

    def locate_element_end(self, element):
        for item in self.timeline.irange(TimingEventBegin(element)):
            if item.element == element and isinstance(item, TimingEventEnd):
                return item
        raise LookupError()

    def lookup_range_on_timeline(self, begin=None, end=None):
        """
        Extract a segment of the timeline and
        :param begin:
        :param end:
        :return: A list of elements in chronological order
        """
        affected_elements = []

        # Coming from the beginning of the timeline in any case
        for item in self.timeline.irange(maximum=end is not None and TimingEvent(None, end) or None):

            if isinstance(item, TimingEventBegin):
                if item.when != end:
                    # Don't take 0 long elements
                    affected_elements.append(item.element)
                continue
            elif isinstance(item, TimingEventEnd):
                if begin is not None and item.when <= begin:
                    # Remove elements, which had ended before the specified range began.
                    if item.element in affected_elements:
                        affected_elements.remove(item.element)
        return affected_elements
