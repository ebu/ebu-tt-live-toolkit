
from pyxb.utils import six
from pyxb.exceptions_ import ValidationError

from .strings import ERR_DOCUMENT_EXTENT_MISSING

class DocumentNotLoadedError(Exception):
    pass


class TimeFormatError(Exception):
    pass


class TimeFormatOverflowError(Exception):
    pass


class XMLParsingFailed(Exception):
    pass


class SemanticValidationError(Exception):
    pass


class EndOfData(Exception):
    pass


class IncompatibleSequenceError(Exception):
    pass


class SequenceNumberAlreadyUsedError(Exception):
    pass


class DocumentDiscardedError(Exception):
    offending_document = None


class SequenceOverridden(Exception):
    pass


class LogicError(Exception):
    pass


class ExtentMissingError(Exception):

    _attribute = None

    def __init__(self, attribute):
        self._attribute = attribute

    def __str__(self):
        return ERR_DOCUMENT_EXTENT_MISSING.format(type=type(self._attribute), value=self._attribute)
