from .base import SubtitleDocument, TimeBase, CloningDocumentSequence
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttm as metadata
from ebu_tt_live.strings import ERR_DOCUMENT_SEQUENCE_MISMATCH
from pyxb import BIND


class EBUTT3Document(SubtitleDocument):

    # The XML binding holding the content of the document
    _ebutt3_content = None

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
    def sequence_number(self):
        return self._ebutt3_content.sequenceNumber

    @sequence_number.setter
    def sequence_number(self, value):
        intvalue = int(value)
        self._ebutt3_content.sequenceNumber = intvalue

    def validate(self):
        self._ebutt3_content.validateBinding()

    def add_region(self, region):
        self._ebutt3_content.validateBinding()

    def add_style(self, style):
        self._ebutt3_content.validateBinding()

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
    _lang = None

    def __init__(self, sequence_identifier, reference_clock, lang):
        self._sequence_identifier = sequence_identifier
        self._reference_clock = reference_clock
        self._lang = lang
        self._last_sequence_number = 0

    @property
    def reference_clock(self):
        return self._reference_clock

    @classmethod
    def create_from_document(cls, document, *args, **kwargs):
        pass

    def new_document(self, *args, **kwargs):
        self._last_sequence_number += 1
        return EBUTT3Document(
            time_base=self._reference_clock.time_base,
            clock_mode=self._reference_clock.clock_mode,
            sequence_identifier=self._sequence_identifier,
            sequence_number=self._last_sequence_number,
            lang=self._lang
        )

    def fork(self, *args, **kwargs):
        pass
