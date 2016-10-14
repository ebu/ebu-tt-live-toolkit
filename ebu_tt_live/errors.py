
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


class StopBranchIteration(Exception):
    """
    Let the iterator know that it can proceed to the next branch. It does not need to traverse the current one any
    further.
    """


class OutsideSegmentError(StopBranchIteration):
    """
    This exception is meant to be raised by the copying functionality to make the iterator know that a particular
    subtree is not meant to be parsed.
    """


class DiscardElement(Exception):
    """
    There is a possibility that an element may become superfluous or lose its value. Such a possibility  can happen
    in segmentation when a p element gets selected because it contains 2 spans but the segment happens to be selecting
    an interval between them so the container ends up being empty and thus should be discarded.
    """