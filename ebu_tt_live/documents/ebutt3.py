from .base import SubtitleDocument, Subtitle, TimeBase
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttm as metadata
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
        return self._ebutt3_content.toDOM().toprettyxml(
            indent='  '
        )
