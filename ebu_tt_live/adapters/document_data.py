
from .base import IDocumentDataAdapter
from ebu_tt_live.documents import EBUTT3EBUTTDConverter, EBUTTDDocument, EBUTT3Document
from ebu_tt_live.clocks.media import MediaClock
import six


class XMLtoEBUTT3Adapter(IDocumentDataAdapter):
    """
    This converter converts the raw XML documents to the EBUTT3Document type.
    """
    _expects = six.string_types
    _provides = EBUTT3Document

    def convert_data(self, data, availability_time=None, **kwargs):
        return EBUTT3Document.create_from_xml(data, availability_time=availability_time), kwargs


class XMLtoEBUTTDAdapter(IDocumentDataAdapter):
    """
    This converter converts the raw XML documents to the EBUTTDDocument type.
    """
    _expects = six.string_types
    _provides = EBUTTDDocument

    def convert_data(self, data, **kwargs):
        return EBUTTDDocument.create_from_xml(data), kwargs


class EBUTTDtoXMLAdapter(IDocumentDataAdapter):
    """
    This converter serializes Document objects to XML
    """
    _expects = EBUTTDDocument
    _provides = six.string_types

    def convert_data(self, data, **kwargs):
        return data.get_xml(), kwargs


class EBUTT3toXMLAdapter(IDocumentDataAdapter):
    """
    This converter deserializes the EBUTT3Document object into xml.
    """

    _expects = EBUTT3Document
    _provides = six.string_types

    def convert_data(self, data, **kwargs):
        kwargs.update({
            'sequence_identifier': data.sequence_identifier,
            'sequence_number': data.sequence_number,
            'availability_time': data.availability_time,
            'time_base': data.time_base
        })
        instance = data.get_xml()
        return instance, kwargs


class EBUTT3toEBUTTDAdapter(IDocumentDataAdapter):
    """
    This converter converts between the EBUTT3Document and the EBUTTDDocument types.
    """
    _expects = EBUTT3Document
    _provides = EBUTTDDocument

    _converter = None

    def __init__(self, media_clock=None):
        if media_clock is None:
            media_clock = MediaClock()
        self._converter = EBUTT3EBUTTDConverter(media_clock=media_clock)

    def convert_data(self, data, **kwargs):
        return EBUTTDDocument.create_from_raw_binding(self._converter.convert_document(data)), kwargs


def get_document_data_adapter(expects, provides):
    """
    Find a matching conversion between 2 document data interfaces.
    :param expects: Data in
    :param provides: Expected interface the data needs to be converted to.
    :return: An adapter instance ready to go.
    """
    return IDocumentDataAdapter.get_registered_impl(expects=expects, provides=provides)()
