import logging
from .base import SubtitleDocument, TimeBase, CloningDocumentSequence
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttm as metadata, TimingValidationMixin
from ebu_tt_live.strings import ERR_DOCUMENT_SEQUENCE_MISMATCH, \
    ERR_DOCUMENT_NOT_COMPATIBLE, ERR_DOCUMENT_NOT_PART_OF_SEQUENCE, \
    ERR_DOCUMENT_SEQUENCE_INCONSISTENCY, DOC_DISCARDED, DOC_TRIMMED
from ebu_tt_live.errors import IncompatibleSequenceError, DocumentDiscardedError, \
    SequenceOverridden
from ebu_tt_live.clocks import get_clock_from_document
from datetime import timedelta
from pyxb import BIND
from sortedcontainers import sortedset
from sortedcontainers import sortedlist


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class TimingEvent(object):
    """
    This class wraps a document and an associated resolved timing event into an object that can be placed
    on the timeline.
    """

    _document = None
    _when = None

    def __init__(self, document, when):
        self._document = document
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
    def document(self):
        return self._document


# R16
class TimingEventBegin(TimingEvent):
    """
    Document resolved begin time
    """

    def __init__(self, document):
        super(TimingEventBegin, self).__init__(
            document=document,
            when=document.computed_begin_time
        )

# R17
class TimingEventEnd(TimingEvent):
    """
    Document resolved end time.
    """
    def __init__(self, document):
        super(TimingEventEnd, self).__init__(
            document=document,
            when=document.computed_end_time
        )


class EBUTT3Document(SubtitleDocument):
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
        # This is assuming availability from the beginning of our time coordinate system.
        availability_time = self.availability_time or timedelta()
        # Run validation
        result = self._ebutt3_content.validateBinding(
            availability_time=availability_time
        )
        # Extract results

        # Begin times

        # Default value for the computed begin time of the document is the active begin time of the body
        # This only changes if the body does not declare a begin time.
        self._computed_begin_time = self._ebutt3_content.body.computed_begin_time
        body_begin = self._ebutt3_content.body.begin
        # This is the earliest computed begin time of any child within body
        begin_limit = result['semantic_dataset']['timing_begin_limit']
        # If the body defines no begin time, the document's computed begin time
        # is the earliest computed begin time of body's children elements (and this
        # applies recursively) How lucky it is that we collected this info during validation :)
        if body_begin is None and begin_limit is not None:
            self._computed_begin_time = begin_limit

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


class EBUTT3DocumentSequence(CloningDocumentSequence):
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
    _timeline = None

    def __init__(self, sequence_identifier, reference_clock, lang):
        self._sequence_identifier = sequence_identifier
        self._reference_clock = reference_clock
        self._lang = lang
        self._last_sequence_number = 0
        # The documents are kept in a sorted set that is sorted by the documents's sequence number
        self._documents = sortedset.SortedSet()
        # The timing events that mark the beginning and end of a document are kept on a timeline,
        # which iw a sorted list. IMPORTANT: Not sorted set as there are overlapping begins and ends.
        self._timeline = sortedlist.SortedListWithKey(key=lambda item: item.when)

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
        if self.sequence_identifier != document.sequence_identifier:
            raise IncompatibleSequenceError(
                ERR_DOCUMENT_NOT_COMPATIBLE
            )
        return True

    def new_document(self, *args, **kwargs):
        self._last_sequence_number += 1
        return EBUTT3Document(
            time_base=self._reference_clock.time_base,
            clock_mode=self._reference_clock.clock_mode,
            sequence_identifier=self._sequence_identifier,
            sequence_number=self._last_sequence_number,
            lang=self._lang
        )

    def _insert_or_discard(self, document):
        """
        This function does the heavy lifting of timing resolution. It inspects the close vicinity in which the
        new document is coming by looking at the timeline in both directions.

        Based on that information it can detect 3 different cases:
          - out of order delivery of documents in which case it inserts and trims the document,
          - sequence override scenario in which case an exception is raised.
          - Document discard scenario in which case the document is already overwritten in the sequence so
            it will not get inserted.

        :raises ValueError, SequenceOverridden, DocumentDiscardedError
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
        for item in self._timeline.irange(
            maximum=this_begins,
            reverse=True
        ):
            # This loop goes backwards and checks for trimmed documents

            # If any found event is higher sequence number we quit
            if item.document.sequence_number > document.sequence_number:
                # Oops we got discarded.... :(
                discarderror = DocumentDiscardedError()
                discarderror.offending_document = item.document
                raise discarderror

            if isinstance(item, TimingEventBegin):
                if not _end_found or _end_found.document != item.document:
                    # This will be trimmed
                    begins_before = item
                # Once a begin event is found we quit
                break
            elif isinstance(item, TimingEventEnd):
                if _end_found:
                    raise ValueError(ERR_DOCUMENT_SEQUENCE_INCONSISTENCY)
                _end_found = item

        for item in self._timeline.irange(this_begins):
            # This loop goes forward looking at offending events
            if isinstance(item, TimingEventEnd):
                ends_after = item
                if ends_after.document != begins_before.document:
                    raise ValueError(ERR_DOCUMENT_SEQUENCE_INCONSISTENCY)

            elif isinstance(item, TimingEventBegin):
                if document.sequence_number > item.document.sequence_number:
                    raise SequenceOverridden()
                if item.document.sequence_number > document.sequence_number:
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
                self._timeline.remove(ends_after)
            else:
                ends_after = TimingEventEnd(begins_before.document)
            ends_after.when = this_begins.when
            document_logger.info(DOC_TRIMMED.format(
                sequence_identifier=begins_before.document.sequence_identifier,
                sequence_number=begins_before.document.sequence_number,
                resolved_begin_time=begins_before.when,
                resolved_end_time=ends_after.when
            ))
            self._timeline.add(ends_after)

        self._insert_document(document, ends=this_ends)

    def _insert_document(self, document, ends=None):
        """
        In the end this function adds the document to the sequence registers.
        :param document:
        :param ends:
        :return:
        """
        self._documents.add(document)
        self._timeline.add(TimingEventBegin(document))
        if ends is not None and ends.when is not None:
            self._timeline.add(ends)
        else:
            computed_end = TimingEventEnd(document)
            if computed_end.when is not None:
                self._timeline.add(computed_end)

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

        for item in self._timeline.irange(resolved_begin):
            if item.document.sequence_number < sequence_number:
                if isinstance(item, TimingEventEnd) and item.document not in discarded_timing_events:
                    # We found the end event of a document whose begin event was not encountered. Meaning that instead
                    # of discarding it we are supposed to trim it. R17
                    continue
                else:
                    discarded_timing_events.setdefault(item.document, []).append(item)

        for item, events in discarded_timing_events.items():
            item.discard_document(resolved_end_time=resolved_begin.when)
            self._documents.remove(item)
            for event in events:
                self._timeline.remove(event)

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
        # TODO: Fix this too hungry
        if document not in self._documents:
            raise LookupError()
        for item in self._timeline.irange(TimingEventBegin(document)):
            if item.document == document and isinstance(item, TimingEventBegin):
                return item
        # This means the document is not part of this sequence
        raise KeyError()

    def resolved_begin_time(self, document):
        return self._find_resolved_begin_event(document).when

    def _find_resolved_end_event(self, document):
        # TODO: Fix this too hungry
        if document not in self._documents:
            raise LookupError()
        for item in self._timeline.irange(TimingEventBegin(document)):
            if item.document == document and isinstance(item, TimingEventEnd):
                return item
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
