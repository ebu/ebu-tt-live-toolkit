
from ebu_tt_live.documents import EBUTT3Document, EBUTTDDocument, EBUTT3EBUTTDConverter
from ebu_tt_live.clocks.media import MediaClock
from .base import CombinedCarriageImpl


class StreamConverter(CombinedCarriageImpl):
    """
    Stream converters, which can convert in a controlled way to/from the carriage mechanism to the
    data-format the node expects. This allows a node to either send/receive raw xml to/from the carriage mechanism or
    a parsed binding instance or a Document object that includes the parsed bindings...etc. The subclasses need to
    implement the convert_data method. If the converter is parameterized the initializer should be extended.
    NOTE: Never forget to call the super() method in the initializer.

    For the sake of flexibility the converters emulate the carriage mechanism interface and the process_document
    function from the Node interface. They are supposed to be chained between the node and the carriage mechanism
    in particular order.

    Example:

        SimpleConsumer(
            carriage_impl=ConverterA(
                carriage_impl=ConverterB(
                    carriage_impl=TwistedConsumerImpl(),
                    ...
                ),
                ...
            ),
            ...
        )

    These converters can be used on input or output side. The convert_data method should not make a difference based
    on direction of transfer. i.e.: The converter always converts the data one way regardless of transfer direction so
    to convert the data back a different converter is needed
    """

    _carriage_impl = None

    def __init__(self, carriage_impl):
        """
        The converter makes connection between these 2 things.

        :param carriage_impl: The carriage mechanism or the next converter
        """
        super(StreamConverter, self).__init__()

        # Propagate the creation of the chain
        self._carriage_impl = carriage_impl
        self._carriage_impl.register(self)

    def on_new_data(self, data):
        # This is the input carriage side. We deliver to a processing the node or another converter.
        self.process_document(document=data)

    def emit_data(self, data):
        # This is the output carriage side. We deliver to a downstream carriage implementation
        converted_data = self.convert_data(data)
        self._carriage_impl.emit_data(data=converted_data)

    def process_document(self, document):
        # Compatibility method to support input carriage chaining
        converted_data = self.convert_data(document)
        self.node.process_document(document=converted_data)

    def convert_data(self, data):
        """
        Subclasses must implement this method
        :param data:
        :return:
        """
        raise NotImplementedError()


class XMLtoEBUTT3DocumentStream(StreamConverter):
    """
    This converter converts the raw XML documents to the EBUTT3Document type.
    """

    def convert_data(self, data):
        return EBUTT3Document.create_from_xml(data)


class XMLtoEBUTTDDocumentStream(StreamConverter):
    """
    This converter converts the raw XML documents to the EBUTTDDocument type.
    """

    def convert_data(self, data):
        return EBUTTDDocument.create_from_xml(data)


class DocumenttoXMLStream(StreamConverter):
    """
    This converter serializes Document objects to XML
    """

    def convert_data(self, data):
        return data.get_xml()


class EBUTT3toEBUTTDStream(StreamConverter):
    """
    This converter converts between the EBUTT3Document and the EBUTTDDocument types.
    """

    _converter = None

    def __init__(self, carriage_impl, media_clock=None):
        super(EBUTT3toEBUTTDStream, self).__init__(carriage_impl)
        if media_clock is None:
            media_clock = MediaClock()
        self._converter = EBUTT3EBUTTDConverter(media_clock=media_clock)

    def convert_data(self, data):
        return EBUTTDDocument.create_from_raw_binding(self._converter.convert_document(data))
