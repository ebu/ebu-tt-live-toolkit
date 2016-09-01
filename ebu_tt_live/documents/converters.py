
from ebu_tt_live.bindings.converters.ebutt3_ebuttd import EBUTT3EBUTTDConverter
from ebu_tt_live.documents.ebuttd import EBUTTDDocument


def ebutt3_to_ebuttd(ebutt3_in):
    """
    This function takes an EBUTT3Document instance and returns the same document as an EBUTTDDocument instance.
    :param ebutt3_in:
    :return:
    """
    ebuttd_bindings = EBUTT3EBUTTDConverter.convert_element(ebutt3_in.binding, dataset={})
    ebuttd_document = EBUTTDDocument.create_from_raw_binding(ebuttd_bindings)
    ebuttd_document.validate()
    return ebuttd_document
