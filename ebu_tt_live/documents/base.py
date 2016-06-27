
from ebu_tt_live.utils import ComparableMixin

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
