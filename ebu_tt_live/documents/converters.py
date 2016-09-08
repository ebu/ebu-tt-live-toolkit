
from ebu_tt_live.bindings.converters.ebutt3_ebuttd import EBUTT3EBUTTDConverter
from ebu_tt_live.documents.ebuttd import EBUTTDDocument


def ebutt3_to_ebuttd(ebutt3_in, media_clock):
    """
    This function takes an EBUTT3Document instance and returns the same document as an EBUTTDDocument instance.
    :param ebutt3_in:
    :return:
    """
    converter = EBUTT3EBUTTDConverter(media_clock=media_clock)
    ebuttd_bindings = converter.convert_element(ebutt3_in.binding, dataset={})
    ebuttd_document = EBUTTDDocument.create_from_raw_binding(ebuttd_bindings)
    ebuttd_document.validate()
    return ebuttd_document
