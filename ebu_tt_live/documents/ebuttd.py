import logging
from xml.dom import minidom
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
    def create_from_xml(cls, xml):
        # NOTE: This is a workaround to make the bindings accept separate root element identities
        # for the same name. tt comes in but we rename it to ttd to make the xsd validate.
        xml_dom = minidom.parseString(xml)
        if xml_dom.documentElement.tagName == 'tt':
            xml_dom.documentElement.tagName = 'ttd'
        instance = cls.create_from_raw_binding(
            binding=bindings.CreateFromDOM(
                xml_dom
            )
        )
        return instance

    @classmethod
    def create_from_raw_binding(cls, binding):
        instance = cls.__new__(cls)
        instance._ebuttd_content = binding
        return instance

    def get_xml(self):
        return self._ebuttd_content.toxml()

    def get_dom(self):
        return self._ebuttd_content.toDOM()
