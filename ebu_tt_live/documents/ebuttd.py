import logging
from .base import SubtitleDocument, TimeBase
from ebu_tt_live import bindings
from ebu_tt_live.bindings.converters.ebutt3_ebuttd import EBUTT3EBUTTDConverter


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class EBUTTDDocument(SubtitleDocument):

    _ebuttd_content = None

    def __init__(self):
        self._ebuttd_content = bindings.ttd()

    def validate(self):
        self._ebuttd_content.validateBinding()

    @classmethod
    def create_from_xml(cls, xml_in):
        document = EBUTTDDocument()
        document._ebuttd_content = bindings.ttd.CreateFromXML(xml_in)

    @classmethod
    def create_from_raw_binding(cls, binding_in):
        document = EBUTTDDocument()
        document._ebuttd_content = binding_in
        return document
