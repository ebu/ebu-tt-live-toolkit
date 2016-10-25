import logging
from .base import SubtitleDocument, TimeBase, CloningDocumentSequence
from .ebutt3_segmentation import EBUTT3Segmenter
from .ebutt3_splicer import EBUTT3Splicer
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttm as metadata, TimingValidationMixin
from ebu_tt_live.strings import ERR_DOCUMENT_SEQUENCE_MISMATCH, \
    ERR_DOCUMENT_NOT_COMPATIBLE, ERR_DOCUMENT_NOT_PART_OF_SEQUENCE, \
    ERR_DOCUMENT_SEQUENCE_INCONSISTENCY, DOC_DISCARDED, DOC_TRIMMED, DOC_REQ_SEGMENT, DOC_SEQ_REQ_SEGMENT, \
    DOC_INSERTED, DOC_SEMANTIC_VALIDATION_SUCCESSFUL
from ebu_tt_live.errors import IncompatibleSequenceError, DocumentDiscardedError, \
    SequenceOverridden
from ebu_tt_live.clocks import get_clock_from_document
from datetime import timedelta
from pyxb import BIND
from sortedcontainers import sortedset
from sortedcontainers import sortedlist
import gc


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


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


class EBUTT3Document(TimelineUtilMixin, SubtitleDocument):
    """
    This class wraps the binding object representation of the XML and provides the features the applications in the
    specification require. e.g:availability time.
    """

    # The XML binding holding the content of the document
    _ebutt3_content = None
    # The availability time can be set by the carriage implementation for
    # example
    _availability_time = None
    _computed_begin_time = None
    _computed_end_time = None

    # These are used when the sequence discarded the documents.
    _resolved_begin_time = None
    _resolved_end_time = None

    # The sequence the document belongs to
    _sequence = None

    def __init__(self, time_base, sequence_number, sequence_identifier, lang, clock_mode=None):
        if not clock_mode and time_base is TimeBase.CLOCK:
            clock_mode = 'local'
        self._ebutt3_content = bindings.tt(
            timeBase=time_base,
            clockMode=clock_mode,
            sequenceIdentifier=sequence_identifier,
            sequenceNumber=sequence_number,
            lang=lang,
            head=BIND(
                metadata.headMetadata_type(
                    metadata.documentMetadata()
                )
            ),
            body=BIND()
        )

        self.validate()

    @classmethod
    def create_from_raw_binding(cls, binding):
        instance = cls.__new__(cls)
        instance._ebutt3_content = binding
        instance.validate()
        return instance

    @classmethod
    def create_from_xml(cls, xml):
        instance = cls.create_from_raw_binding(
            binding=bindings.CreateFromDocument(
                xml_text=xml
            )
        )
        return instance

    def _cmp_key(self):
        return self.sequence_number

    def _cmp_checks(self, other):
        if self.sequence_identifier != other.sequence_identifier:
            raise ValueError(ERR_DOCUMENT_SEQUENCE_MISMATCH)

    @property
    def sequence_identifier(self):
        return self._ebutt3_content.sequenceIdentifier

    @sequence_identifier.setter
    def sequence_identifier(self, value):
        self._ebutt3_content.sequenceIdentifier = value

    @property
    def lang(self):
        return self._ebutt3_content.lang

    @property
    def clock_mode(self):
        return self._ebutt3_content.clockMode

    @property
    def sequence(self):
        if self._sequence is None:
            raise ValueError(ERR_DOCUMENT_NOT_PART_OF_SEQUENCE)
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        if value.sequence_identifier != self.sequence_identifier:
            raise ValueError(ERR_DOCUMENT_SEQUENCE_MISMATCH)
        self._sequence = value

    @property
    def sequence_number(self):
        return self._ebutt3_content.sequenceNumber

    @sequence_number.setter
    def sequence_number(self, value):
        intvalue = int(value)
        self._ebutt3_content.sequenceNumber = intvalue

    @property
    def availability_time(self):
        return self._availability_time

    @availability_time.setter
    def availability_time(self, value):
        if not isinstance(value, timedelta):
            raise TypeError
        self._availability_time = value
        self.validate()

    @property
    def computed_begin_time(self):
        return self._computed_begin_time

    @property
    def computed_end_time(self):
        return self._computed_end_time

    @property
    def resolved_begin_time(self):
        if self._resolved_begin_time is not None:
            return self._resolved_begin_time
        else:
            return self.sequence.resolved_begin_time(self)

    def discard_document(self, resolved_end_time):
        """
        This function discards the document by setting a resolved end time
        before the document begins.
        :param resolved_end_time:
        """
        if resolved_end_time > self.computed_begin_time:
            raise ValueError()
        document_logger.info(DOC_DISCARDED.format(
            sequence_identifier=self.sequence_identifier,
            sequence_number=self.sequence_number)
        )
        self._resolved_end_time = resolved_end_time
        self._resolved_begin_time = self.computed_begin_time

    @property
    def resolved_end_time(self):
        if self._resolved_end_time is not None:
            return self._resolved_end_time
        else:
            return self.sequence.resolved_end_time(self)

    @property
    def time_base(self):
        return self._ebutt3_content.timeBase

    @property
    def discarded(self):
        return self.resolved_begin_time >= self.resolved_end_time

    def validate(self):
        # Reset timeline
        self.reset_timeline()
        # This is assuming availability from the beginning of our time coordinate system.
        availability_time = self.availability_time or timedelta()
        # Run validation
        result = self._ebutt3_content.validateBinding(
            availability_time=availability_time,
            document=self
        )

        document_logger.debug(
            DOC_SEMANTIC_VALIDATION_SUCCESSFUL.format(
                sequence_identifier=self.sequence_identifier,
                sequence_number=self.sequence_number
            )
        )
        # Extract results

        # Begin times

        # Default value for the computed begin time of the document is the active begin time of the body
        # This only changes if the body does not declare a begin time.
        self._computed_begin_time = self._ebutt3_content.body.computed_begin_time

        # End times
        self._computed_end_time = self._ebutt3_content.body.computed_end_time

    def add_div(self, div):
        body = self._ebutt3_content.body
        body.append(div)

    def set_begin(self, begin):
        self._ebutt3_content.body.begin = begin

    def set_end(self, end):
        self._ebutt3_content.body.end = end

    def set_dur(self, dur):
        self._ebutt3_content.body.dur = dur

    @property
    def binding(self):
        return self._ebutt3_content

    def get_xml(self):
        return self._ebutt3_content.toxml()

    def get_dom(self):
        return self._ebutt3_content.toDOM()

    def get_element_by_id(self, elem_id, elem_type=None):
        return self.binding.get_element_by_id(elem_id=elem_id, elem_type=elem_type)

    def extract_segment(self, begin=None, end=None, deconflict_ids=False):
        """
        Create a valid ebutt3 document subset. As it collects data it will also prefix the ids in the document with
        the document sequence number so that later merge does not have collision.

        :param begin:
        :param end:
        :param deconflict_ids: prevent id clash across documents by prefixing the IDs
        :return: EBUTT3Document
        """
        document_logger.info(
            DOC_REQ_SEGMENT.format(
                sequence_identifier=self.sequence_identifier,
                sequence_number=self.sequence_number,
                begin=begin,
                end=end
            )
        )
        segmenter = EBUTT3Segmenter(self, begin=begin, end=end, deconflict_ids=deconflict_ids)
        return EBUTT3Document.create_from_raw_binding(segmenter.segment)

    def cleanup(self):
        """
        This function is meant to get rid of all the validation added data that may be blocking garbage collection of
        the objects.
        :return:
        """
        self.reset_timeline()


class EBUTT3DocumentSequence(TimelineUtilMixin, CloningDocumentSequence):
    """
    EBU-TT Live specific document sequence. It maps the documents based on their sequence numbers and timing attributes.

    The sequence object can be used in 2 different modes:
      - It can be used to produce a sequence(i.e.: new_document method)
      - as well as it is the pivotal point of the consumer use-case when the document timings need to be resolved.
        (i.e.: add_document method.

    The sequence is responsible to keep the documents ordered and filter those documents out, which were eventually
    overwritten. It ensures that at any given time exactly 0 or 1 document is active (R14).
    """

    _sequence_identifier = None
    _last_sequence_number = None
    _reference_clock = None
    _time_base = None
    _clock_mode = None
    _lang = None
    _documents = None

    def __init__(self, sequence_identifier, reference_clock, lang):
        self._sequence_identifier = sequence_identifier
        self._reference_clock = reference_clock
        self._lang = lang
        self._last_sequence_number = 0
        # The documents are kept in a sorted set that is sorted by the documents's sequence number
        self._documents = sortedset.SortedSet()

    @property
    def reference_clock(self):
        return self._reference_clock

    @property
    def sequence_identifier(self):
        return self._sequence_identifier

    @property
    def last_sequence_number(self):
        return self._last_sequence_number

    @last_sequence_number.setter
    def last_sequence_number(self, value):
        self._last_sequence_number = value

    @classmethod
    def create_from_document(cls, document, *args, **kwargs):
        if not isinstance(document, EBUTT3Document):
            raise ValueError()
        return cls(
            sequence_identifier=kwargs.get('sequence_identifier', document.sequence_identifier),
            reference_clock=kwargs.get('reference_clock', get_clock_from_document(document)),
            lang=kwargs.get('lang', document.lang)
        )

    def _check_document_compatibility(self, document):
        if self.sequence_identifier != document.sequence_identifier or \
                self._reference_clock.time_base != document.time_base:
            raise IncompatibleSequenceError(
                ERR_DOCUMENT_NOT_COMPATIBLE
            )
        if self._reference_clock.time_base == 'clock':
            if self._reference_clock.clock_mode != document.clock_mode:
                raise IncompatibleSequenceError(
                    ERR_DOCUMENT_NOT_COMPATIBLE
                )
        return True

    def create_compatible_document(self, *args, **kwargs):
        """
        This utility function is used by the converter to extract segments and by the new_document function.

        :param args:
        :param kwargs:
        :return:
        """
        return EBUTT3Document(
            time_base=self._reference_clock.time_base,
            clock_mode=self._reference_clock.clock_mode,
            sequence_identifier=self._sequence_identifier,
            sequence_number=self._last_sequence_number,
            lang=self._lang
        )

    def new_document(self, *args, **kwargs):
        self._last_sequence_number += 1
        return self.create_compatible_document()

    def _insert_or_discard(self, document):
        """
        This function does the heavy lifting of timing resolution. It inspects the close vicinity in which the
        new document is coming by looking at the timeline in both directions.

        Based on that information it can detect 3 different cases:
          - out of order delivery of documents in which case it inserts and trims the document,
          - sequence override scenario in which case an exception is raised.
          - Document discard scenario in which case the document is already overwritten in the sequence so
            it will not get inserted.

        :raises: ValueError, SequenceOverridden, DocumentDiscardedError
        """
        # Our document's begin and end times. Initially they correspond with the computed document begin- and end times.
        this_begins = TimingEventBegin(document)
        this_ends = TimingEventEnd(document)
        # The one this document might trim
        begins_before = None
        # The one this document definitely trims
        ends_after = None
        # The one that will trim this document. One with a higher seq number
        trims_this = None

        _end_found = False
        for item in self.timeline.irange(
            maximum=this_begins,
            reverse=True
        ):
            # This loop goes backwards and checks for trimmed documents

            # If any found event is higher sequence number we quit
            if item.element.sequence_number > document.sequence_number:
                # Oops we got discarded.... :(
                discarderror = DocumentDiscardedError()
                discarderror.offending_document = item.element
                raise discarderror

            if isinstance(item, TimingEventBegin):
                if not _end_found or _end_found.element != item.element:
                    # This will be trimmed
                    begins_before = item
                # Once a begin event is found we quit
                break
            elif isinstance(item, TimingEventEnd):
                if _end_found:
                    raise ValueError(ERR_DOCUMENT_SEQUENCE_INCONSISTENCY)
                _end_found = item

        for item in self.timeline.irange(this_begins):
            # This loop goes forward looking at offending events
            if isinstance(item, TimingEventEnd):
                ends_after = item
                if begins_before and ends_after.element != begins_before.element and ends_after.when != begins_before.when:
                    raise ValueError(ERR_DOCUMENT_SEQUENCE_INCONSISTENCY)

            elif isinstance(item, TimingEventBegin):
                if document.sequence_number > item.element.sequence_number:
                    raise SequenceOverridden()
                if item.element.sequence_number > document.sequence_number:
                    #This means our document may get trimmed into shape
                    if this_ends.when > item.when:
                        trims_this = item
                    break

        if trims_this:
            # Trim this one. This happens with out of order delivery.
            this_ends.when = trims_this.when
            document_logger.info(DOC_TRIMMED.format(
                sequence_identifier=document.sequence_identifier,
                sequence_number=document.sequence_number,
                resolved_begin_time=this_begins.when,
                resolved_end_time=this_ends.when
            ))
        if begins_before:
            # Move up previous document's end R17
            if ends_after:
                self.timeline.remove(ends_after)
            else:
                ends_after = TimingEventEnd(begins_before.element)
            ends_after.when = this_begins.when
            document_logger.info(DOC_TRIMMED.format(
                sequence_identifier=begins_before.element.sequence_identifier,
                sequence_number=begins_before.element.sequence_number,
                resolved_begin_time=begins_before.when,
                resolved_end_time=ends_after.when
            ))
            self.timeline.add(ends_after)

        self._insert_document(document, ends=this_ends)

    def _insert_document(self, document, ends=None):
        """
        In the end this function adds the document to the sequence registers.

        :param document:
        :param ends:
        :return:
        """
        self._documents.add(document)
        self.timeline.add(TimingEventBegin(document))
        if ends is not None and ends.when is not None:
            self.timeline.add(ends)
        else:
            computed_end = TimingEventEnd(document)
            if computed_end.when is not None:
                self.timeline.add(computed_end)

        document_logger.info(DOC_INSERTED.format(
            sequence_identifier=document.sequence_identifier,
            sequence_number=document.sequence_number
        ))

    def _override_sequence(self, document):
        """
        This function clears the timeline and the associated documents after the document in the parameter.
        This happens when a document with a higher sequence number is added preceding some other documents with lower
        sequence numbers.

        :param document:
        :return:
        """
        discarded_timing_events = {}

        sequence_number = document.sequence_number
        resolved_begin = TimingEventBegin(document)

        for item in self.timeline.irange(resolved_begin):
            if item.element.sequence_number < sequence_number:
                if isinstance(item, TimingEventEnd) and item.element not in discarded_timing_events:
                    # We found the end event of a document whose begin event was not encountered. Meaning that instead
                    # of discarding it we are supposed to trim it. R17
                    continue
                else:
                    discarded_timing_events.setdefault(item.element, []).append(item)

        for item, events in discarded_timing_events.items():
            item.discard_document(resolved_end_time=resolved_begin.when)
            self._documents.remove(item)
            for event in events:
                self.timeline.remove(event)

    def discard_before(self, document):
        """
        This function gets rid of old documents we do not wish to keep any longer.
        :param document: The document up to which we would like to discard things
        :return:
        """
        discarded_timing_events = {}
        resolved_begin = TimingEventBegin(document)
        discard_time = timedelta()

        for item in self.timeline.irange(maximum=resolved_begin, inclusive=(True, True)):
            if item.element != document:
                discarded_timing_events.setdefault(item.element, []).append(item)

        for item, events in discarded_timing_events.items():
            item.discard_document(resolved_end_time=discard_time)
            self._documents.remove(item)
            for event in events:
                self.timeline.remove(event)
            del item
        del discarded_timing_events

    def add_document(self, document):
        self._check_document_compatibility(document)
        document.sequence = self

        # Let's create space for the document
        try:
            self._insert_or_discard(document)
        except SequenceOverridden:
            # First we fix the timeline
            self._override_sequence(document)
            # And retry the insertion operation
            self._insert_or_discard(document)
        except DocumentDiscardedError as exc:
            document.discard_document(resolved_end_time=exc.offending_document.resolved_begin_time)

        if document.sequence_number > self._last_sequence_number:
            self._last_sequence_number = document.sequence_number

    def get_document(self, seq_id):
        return self._documents[seq_id]

    def _find_resolved_begin_event(self, document):
        if document not in self._documents:
            raise LookupError()
        try:
            item = self.locate_element_begin(document)
            return item
        except LookupError:
            # This means the document is not part of this sequence
            raise KeyError()

    def resolved_begin_time(self, document):
        return self._find_resolved_begin_event(document).when

    def _find_resolved_end_event(self, document):
        if document not in self._documents:
            raise LookupError()
        try:
            item = self.locate_element_end(document)
            return item
        except LookupError:
            pass
        if document.computed_end_time is not None:
            # This means we have consistency issues in the timeline
            raise LookupError(ERR_DOCUMENT_SEQUENCE_INCONSISTENCY)
        # This means this document has no computed end time nor it is trimmed
        return None

    def resolved_end_time(self, document):
        item = self._find_resolved_end_event(document)
        return item and item.when or None

    def fork(self, *args, **kwargs):
        pass

    def extract_segment(self, begin=None, end=None, sequence_number=None, discard=False):
        """
        Extract the subtitles from the sequence in the given timeframe. The return value is one
        merged EBUTT3Document

        :param begin:
        :param end:
        :return: EBUTT3Document
        """
        document_logger.info(
            DOC_SEQ_REQ_SEGMENT.format(
                sequence_identifier=self.sequence_identifier,
                begin=begin,
                end=end
            )
        )
        affected_documents = self.lookup_range_on_timeline(begin=begin, end=end)

        document_segments = []

        for doc in affected_documents:
            doc_ending = doc.resolved_end_time
            if end is not None:
                if doc_ending is None or end < doc_ending:
                    doc_ending = end
            # Check only til resolved end, otherwise there will be unwanted parallel elements
            try:
                doc_segment = doc.extract_segment(begin=begin, end=doc_ending, deconflict_ids=True)
                document_segments.append(doc_segment)
            except Exception as err:
                log.error(
                    'Error extracting document segment from {}__{}'.format(
                        doc.sequence_identifier, doc.sequence_number
                    )
                )
                log.error(err)
                
            begin = doc_ending

        if not document_segments:
            # TODO: This is good question what now? no documents found for range
            return None

        splicer = EBUTT3Splicer(
            sequence_identifier='{}_resegmented'.format(self.sequence_identifier),
            sequence_number=sequence_number is not None or 1,
            document_segments=document_segments
        )

        document = EBUTT3Document.create_from_raw_binding(splicer.spliced_document)

        if discard is True and affected_documents:
            self.discard_before(affected_documents[-1])

        return document

    def cleanup(self):
        self.reset_timeline()
        del self._documents
