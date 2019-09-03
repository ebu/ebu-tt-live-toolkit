
from ebu_tt_live.bindings.converters.ebutt3_ebuttd import EBUTT3EBUTTDConverter
from ebu_tt_live.documents.ebuttd import EBUTTDDocument
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from subprocess import Popen, PIPE
from ebu_tt_live.node.denester import Denester
import tempfile
import os
import logging


log = logging.getLogger(__name__)


def ebutt3_to_ebuttd(ebutt3_in, media_clock):
    """
    This function takes an EBUTT3Document instance and returns the same document as an EBUTTDDocument instance.
    :param ebutt3_in:
    :return:
    """
    #print(ebutt3_in.get_xml())
    converter = EBUTT3EBUTTDConverter(media_clock=media_clock)
    doc_xml = Denester.denest(ebutt3_in).get_xml()
    ebutt3_doc = EBUTT3Document.create_from_xml(doc_xml)
    ebuttd_bindings = converter.convert_document(ebutt3_doc.binding)
    ebuttd_document = EBUTTDDocument.create_from_raw_binding(ebuttd_bindings)
    ebuttd_document.validate()
    return ebuttd_document
