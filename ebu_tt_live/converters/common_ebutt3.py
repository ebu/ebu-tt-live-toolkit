
from .base import ICommonReader, IEBUTT3Writer, implementer
from ebu_tt_live.errors import DocumentNotLoadedError
from ebu_tt_live.strings import ERR_CONV_NO_INPUT


@implementer(ICommonReader, IEBUTT3Writer)
class CommonToEBUTT3Converter(object):
    _document = None

    def get_xml(self):
        if not self._document:
            raise DocumentNotLoadedError(ERR_CONV_NO_INPUT)

        self._document.toDOM().toxml(pretty="  ")

    def load_document(self, document):
        # TODO: validation could happen around here
        self._document = document
