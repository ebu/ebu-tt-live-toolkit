
from ebu_tt_live.utils import ComparableMixin
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttlm as ebuttlm

# NOTE: Some of the code below includes handling of SMPTE time base, which was removed from version 1.0 of the specification.

class TimeBase(object):
    SMPTE = 'smpte'
    MEDIA = 'media'
    CLOCK = 'clock'


class SubtitleDocument(ComparableMixin):

    def __init__(self):
        raise NotImplementedError('This is an abstract class')

    def validate(self):
        raise NotImplementedError()


class DocumentSequence(object):
    """
    Base class that facilitates most production-related workflows.
    The document stream should maintain the consistency across critical document attributes. It should maintain
    all sorts of counters and static information. It plays a key role in the validation of an outgoing stream of
    subtitle documents.
    """

    def new_document(self, *args, **kwargs):
        """
        Create a new document with the stream defaults
        :param args:
        :param kwargs: parameter override to constructor
        :return: a new document
        """
        raise NotImplementedError()

    def add_document(self, document):
        """
        Add the document to the sequence on the consumer side of things. This will put the document on the timeline
        and validate the sequence in terms of timing resolution.
        :param document:
        :raises IncompatibleSequenceError meaning that the document cannot be part of this sequence for
        it does not match the semantics of the sequence.
        """
        raise NotImplementedError()

    def get_document(self, seq_id):
        """
        Retrieve document by sequence number
        :param seq_id:
        :return: a document
        :raises: KeyError meaning the document is not in the sequence
        """
        raise NotImplementedError()

    def __getitem__(self, item):
        return self.get_document(seq_id=item)

    def fork(self, *args, **kwargs):
        """
        Create a new stream with modified arguments.
        :param args:
        :param kwargs: parameter override to constructor
        :return: a new documentstream instance
        """
        raise NotImplementedError()


class CloningDocumentSequence(DocumentSequence):
    """
    Base class that picks up a document and creates an appropriate stream based on it.
    Bear in mind continuation/revision or reproduction of a received document stream.
    """

    @classmethod
    def create_from_document(cls, document, *args, **kwargs):
        """
        Extract data from document
        :param document:
        :param args:
        :param kwargs: parameter override to constructor
        :return:
        """
        raise NotImplementedError()


class EBUTTDocumentBase(object):
    message_type_mapping = {}

    def get_xml(self):
        raise NotImplementedError()

    def get_dom(self):
        raise NotImplementedError()

    @classmethod
    def create_from_xml(cls, xml):
        instance = bindings.CreateFromDocument(
            xml_text=xml
        )
        if isinstance(instance, ebuttlm.message_type):
            return cls.message_type_mapping[instance.header.type].create_from_raw_binding(instance)

    @classmethod
    def create_from_raw_binding(cls, **kwargs):
        raise NotImplementedError()