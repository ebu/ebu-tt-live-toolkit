
from .base import IDocumentDataAdapter
from ebu_tt_live.documents import EBUTT3EBUTTDConverter, EBUTTDDocument, EBUTT3Document
from ebu_tt_live.clocks.media import MediaClock


class XMLtoEBUTT3Adapter(IDocumentDataAdapter):
    """
    This converter converts the raw XML documents to the EBUTT3Document type.
    """

    def convert_data(self, data, **kwargs):
        return EBUTT3Document.create_from_xml(data), kwargs


class XMLtoEBUTTDAdapter(IDocumentDataAdapter):
    """
    This converter converts the raw XML documents to the EBUTTDDocument type.
    """

    def convert_data(self, data, **kwargs):
        return EBUTTDDocument.create_from_xml(data), kwargs


class EBUTTDtoXMLAdapter(IDocumentDataAdapter):
    """
    This converter serializes Document objects to XML
    """

    def convert_data(self, data, **kwargs):
        return data.get_xml(), kwargs


class EBUTT3toXMLAdapter(IDocumentDataAdapter):

    def convert_data(self, data, **kwargs):
        kwargs.update({
            'sequence_identifier': data.sequence_identifier,
            'sequence_number': data.sequence_number,
            'availability_time': data.availability_time
        })
        instance = data.get_xml()
        return instance, kwargs


class EBUTT3toEBUTTDAdapter(IDocumentDataAdapter):
    """
    This converter converts between the EBUTT3Document and the EBUTTDDocument types.
    """

    _converter = None

    def __init__(self, media_clock=None):
        if media_clock is None:
            media_clock = MediaClock()
        self._converter = EBUTT3EBUTTDConverter(media_clock=media_clock)

    def convert_data(self, data, **kwargs):
        return EBUTTDDocument.create_from_raw_binding(self._converter.convert_document(data)), kwargs
