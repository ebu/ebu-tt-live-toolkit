from ebu_tt_live.documents.ebutt1 import EBUTT1Document
from .base import IDocumentDataAdapter
from ebu_tt_live.documents import EBUTT3EBUTTDConverter, EBUTTDDocument, EBUTT3Document, EBUTTAuthorsGroupControlRequest
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.errors import UnexpectedSequenceIdentifierError
from ebu_tt_live.bindings import CreateFromDocument, tt_type, tt1_tt_type
import six
import logging


log = logging.getLogger(__name__)


class XMLtoEBUTT3Adapter(IDocumentDataAdapter):
    """
    This converter converts the raw XML documents to the EBUTT3Document type.
    """
    _expects = six.text_type
    _provides = EBUTT3Document

    def convert_data(self, data, availability_time=None, sequence_identifier=None, **kwargs):
        EBUTT3Document.load_types_for_document()
        binding_inst = CreateFromDocument(xml_text=data)
        if isinstance(binding_inst, tt_type):
            doc = EBUTT3Document.create_from_raw_binding(
                binding_inst,
                availability_time=availability_time
            )
        else:
            # If not an ebutt live document then a message
            doc = EBUTTAuthorsGroupControlRequest.create_from_raw_binding(
                binding_inst,
                availability_time=availability_time
            )

        if sequence_identifier is not None and sequence_identifier != doc.sequence_identifier:
            log.error(
                'Sequence identifier mismatch found: {} != {}'.format(sequence_identifier, doc.sequence_identifier)
            )
            raise UnexpectedSequenceIdentifierError()
        kwargs.update(dict(
            raw_xml=data
        ))
        return doc, kwargs


class XMLtoEBUTT1Adapter(IDocumentDataAdapter):
    """
    This converter converts the raw XML documents to the EBUTT1Document type.
    """
    _expects = six.text_type
    _provides = EBUTT1Document

    def convert_data(self, data, availability_time=None, sequence_identifier=None, **kwargs):
        EBUTT1Document.load_types_for_document()
        binding_inst = CreateFromDocument(xml_text=data)
        if isinstance(binding_inst, tt1_tt_type):
            doc = EBUTT1Document.create_from_raw_binding(
                binding_inst
            )

        kwargs.update(dict(
            raw_xml=data
        ))
        return doc, kwargs


class XMLtoEBUTTDAdapter(IDocumentDataAdapter):
    """
    This converter converts the raw XML documents to the EBUTTDDocument type.
    """
    _expects = six.text_type
    _provides = EBUTTDDocument

    def convert_data(self, data, **kwargs):
        return EBUTTDDocument.create_from_xml(data), kwargs


class EBUTTDtoXMLAdapter(IDocumentDataAdapter):
    """
    This converter serializes Document objects to XML
    """
    _expects = EBUTTDDocument
    _provides = six.text_type

    def convert_data(self, data, **kwargs):
        return data.get_xml(), kwargs


class EBUTT3toXMLAdapter(IDocumentDataAdapter):
    """
    This converter deserializes the EBUTT3Document object into xml.
    """

    _expects = EBUTT3Document
    _provides = six.text_type

    def convert_data(self, data, **kwargs):
        if isinstance(data, EBUTT3Document):
            kwargs.update({
                'sequence_identifier': data.sequence_identifier,
                'sequence_number': data.sequence_number,
                'availability_time': data.availability_time,
                'time_base': data.time_base,
                'clock_mode': data.clock_mode
            })
        else:
            kwargs.update({
                'sequence_identifier': data.sequence_identifier,
                'availability_time': data.availability_time,
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
        return EBUTTDDocument.create_from_raw_binding(self._converter.convert_document(data.binding)), kwargs


def get_document_data_adapter(expects, provides):
    """
    Find a matching conversion between 2 document data interfaces.
    :param expects: Data in
    :param provides: Expected interface the data needs to be converted to.
    :return: An adapter instance ready to go.
    """
    return IDocumentDataAdapter.get_registered_impl(expects=expects, provides=provides)()
