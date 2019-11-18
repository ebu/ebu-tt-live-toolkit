
from ebu_tt_live.bindings.converters.ebutt3_ebuttd import EBUTT3EBUTTDConverter
from ebu_tt_live.bindings.converters.ebutt1_ebutt3 import EBUTT1EBUTT3Converter
from ebu_tt_live.bindings.converters.timedelta_converter import \
    FixedOffsetSMPTEtoTimedeltaConverter

from ebu_tt_live.documents.ebuttd import EBUTTDDocument
from ebu_tt_live.documents.ebutt1 import EBUTT1Document
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
import logging


log = logging.getLogger(__name__)


def ebutt3_to_ebuttd(ebutt3_in, media_clock):
    """
    This function takes an EBUTT3Document instance and returns the same
    document as an EBUTTDDocument instance.
    :param ebutt3_in:
    :return:
    """

    converter = EBUTT3EBUTTDConverter(media_clock=media_clock)
    # Here we need a thing that makes sure that the times in the input 
    # document do not depend on a body@dur attribute, and that they are
    # absolutised, so a body with no begin or end time but with a dur
    # gets fixed into a body with an end time, which gives the
    # denester an easier job.
    doc_xml = ebutt3_in.get_xml()
    ebutt3_doc = EBUTT3Document.create_from_xml(doc_xml)
    ebuttd_bindings = converter.convert_document(ebutt3_doc.binding)
    ebuttd_document = EBUTTDDocument.create_from_raw_binding(ebuttd_bindings)
    ebuttd_document.validate()
    return ebuttd_document


def ebutt1_to_ebutt3(ebutt1_in, 
                     sequence_id,
                     use_doc_id_as_seq_id,
                     smpte_start_of_programme=None):
    """
    Convert an EBUTT1Document instance to an EBUTT3Document instance.

    This code is (currently!) the same as the code in
    :py:class:`ebu_tt_live.node.ebutt1_ebutt3_producer.EBUTT1EBUTT3ProducerNode`
    so it probably makes sense to use one of those rather than this utility
    function.
    
    :param EBUTT1Document ebutt1_in: The EBU-TT Part 1 document to convert
    :param string sequence_id: The default sequence identifier to use for the output
    :param Boolean use_doc_id_as_seq_id: Whether to use the ebuttm:documentIdentifier element value as the output sequence identifier, if it exists
    :param string smpte_start_of_programme: SMPTE timecode for the start of programme, if known - if present, will override the ebuttm:documentStartOfProgramme metadata.
    :return EBUTT3Document: The converted EBU-TT Part 3 document
    """
    converter = EBUTT1EBUTT3Converter(
        sequence_id=sequence_id, 
        use_doc_id_as_seq_id=use_doc_id_as_seq_id)
    doc_xml = ebutt1_in.get_xml()
    ebutt1_doc = EBUTT1Document.create_from_xml(doc_xml)

    smpte_converter = None
    if ebutt1_doc.binding.timeBase == 'smpte':
        start_of_programme = '00:00:00:00'
        if smpte_start_of_programme is None:
            head_metadata = ebutt1_doc.binding.head.metadata
            if head_metadata:
                doc_metadata = head_metadata.documentMetadata
                if doc_metadata and doc_metadata.documentStartOfProgramme:
                    start_of_programme = doc_metadata.documentStartOfProgramme
        else:
            start_of_programme = smpte_start_of_programme

        smpte_converter = \
            FixedOffsetSMPTEtoTimedeltaConverter(
                start_of_programme,
                ebutt1_doc.binding.frameRate,
                ebutt1_doc.binding.frameRateMultiplier,
                ebutt1_doc.binding.dropMode
            )

    ebutt3_bindings = converter.convert_document(
        ebutt1_doc.binding,
        dataset=None,
        smpte_to_timedelta_converter=smpte_converter)
    ebutt3_document = EBUTT3Document.create_from_raw_binding(ebutt3_bindings)
    ebutt3_document.validate()
    return ebutt3_document
