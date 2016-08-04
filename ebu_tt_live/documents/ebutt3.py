import logging
from .base import SubtitleDocument, TimeBase, CloningDocumentSequence
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttm as metadata
from ebu_tt_live.strings import ERR_DOCUMENT_SEQUENCE_MISMATCH, ERR_DOCUMENT_NOT_COMPATIBLE, ERR_DOCUMENT_NOT_PART_OF_SEQUENCE
from ebu_tt_live.errors import IncompatibleSequenceError
from ebu_tt_live.clocks import get_clock_from_document
from datetime import timedelta
from pyxb import BIND
from sortedcontainers import sortedset
from sortedcontainers import sortedlist


log = logging.getLogger(__name__)


class TimingEvent(object):

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


class TimingEventBegin(TimingEvent):

    def __init__(self, document):
        super(TimingEventBegin, self).__init__(document, document.computed_begin_time)


class TimingEventEnd(TimingEvent):

    def __init__(self, document):
        super(TimingEventEnd, self).__init__(document, document.computed_end_time)


class EBUTT3Document(SubtitleDocument):

    # The XML binding holding the content of the document
    _ebutt3_content = None
    # The availability time can be set by the carriage implementation for
    # example
    _availability_time = None
    _computed_begin_time = None
    _computed_end_time = None
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
        return self.sequence.resolved_begin_time(self)

    @property
    def resolved_end_time(self):
        return self.sequence.resolved_end_time(self)

    @property
    def time_base(self):
        return self._ebutt3_content.timeBase

    def validate(self):
        # This is assuming availability from the beginning of our time coordinate system.
        availability_time = self.availability_time or timedelta()
        # Run validation
        result = self._ebutt3_content.validateBinding(
            availability_time=availability_time
        )
        # Extract results

        # Begin times
        computed_begin = result['semantic_dataset']['timing_computed_begin']
        if computed_begin is not None:
            self._computed_begin_time = max(availability_time, computed_begin)
        else:
            self._computed_begin_time = availability_time

        # End times
        self._computed_end_time = result['semantic_dataset']['timing_computed_end']

    def add_div(self, div):
        body = self._ebutt3_content.body
        body.append(div)

    def set_begin(self, begin):
        self._ebutt3_content.body.begin = begin

    def set_end(self, end):
        self._ebutt3_content.body.end = end

    def set_dur(self, dur):
        self._ebutt3_content.body.dur = dur

    def get_xml(self):
        return self._ebutt3_content.toxml()


class EBUTT3DocumentSequence(CloningDocumentSequence):

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
        self._documents = sortedset.SortedSet()
        self._timeline = sortedlist.SortedList()

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

    def add_document(self, document):
        self._check_document_compatibility(document)
        document.sequence = self
        self._documents.add(document)
        if document.computed_begin_time is not None:
            log.debug('Creating begin event for {} at {}'.format(
                document, document.computed_begin_time
            ))
            self._timeline.add(TimingEventBegin(document))
        if document.computed_end_time is not None:
            log.debug('Creating end event for {} at {}'.format(
                document, document.computed_end_time
            ))
            self._timeline.add(TimingEventEnd(document))

    def get_document(self, seq_id):
        return self._documents[seq_id]

    def resolved_begin_time(self, document):
        return timedelta()

    def resolved_end_time(self, document):
        return timedelta()

    def fork(self, *args, **kwargs):
        pass
