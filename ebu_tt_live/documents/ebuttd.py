import logging
from .base import SubtitleDocument, TimeBase
from ebu_tt_live import bindings


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class EBUTTDDocument(SubtitleDocument):

    def __init__(self):
        pass

    def validate(self):
        pass

    @classmethod
    def create_from_xml(cls):
        return EBUTTDDocument()

    @classmethod
    def create_from_raw_binding(cls):
        return EBUTTDDocument()
