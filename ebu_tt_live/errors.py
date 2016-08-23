
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
