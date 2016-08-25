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

    @classmethod
    def create_from_ebutt3(cls, ebutt3_in):
        ebuttd_bindings = EBUTT3EBUTTDConverter.convert_element(ebutt3_in.binding)
        return cls.create_from_raw_binding(ebuttd_bindings)
