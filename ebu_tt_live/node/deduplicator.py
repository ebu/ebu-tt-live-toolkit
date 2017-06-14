from .base import AbstractCombinedNode
from ebu_tt_live.documents import EBUTT3DocumentSequence, EBUTT3Document
from ebu_tt_live.bindings import _ebuttm as metadata
from ebu_tt_live.bindings.pyxb_utils import RecursiveOperation, StopBranchIteration
from ebu_tt_live.strings import DOC_RECEIVED
from ebu_tt_live.errors import SequenceNumberCollisionError
from ebu_tt_live.errors import UnexpectedSequenceIdentifierError
from pyxb.binding.basis import NonElementContent, ElementContent
from pyxb import BIND
from ebu_tt_live import bindings
import logging


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class DeDuplicatorNode(AbstractCombinedNode):
    _original_styles = []
    _original_regions = []
    _mirror_styles_no_id = []
    _new_style_list = [[],[],[],[]]
    _new_region_list = [[],[],[],[]]
    _styling_element = None
    _region_element = None
    _span_style_id = None
    _region_style_id = None
    _sequence_identifier = None
    # _sequence_number = None
    _expects = EBUTT3Document
    _provides = EBUTT3Document

    def __init__(self, node_id, sequence_identifier, consumer_carriage=None, producer_carriage=None):
        super(DeDuplicatorNode, self).__init__(
            node_id=node_id,
            consumer_carriage=consumer_carriage,
            producer_carriage=producer_carriage
        )
        self._sequence_identifier = sequence_identifier
        # self._sequence_number = sequence_number

    def process_document(self, document, **kwargs):
        if self.is_document(document):

            if document.sequence_identifier == self._sequence_identifier:
                raise UnexpectedSequenceIdentifierError()

            if self.check_if_document_seen(document=document):

                self.limit_sequence_to_one(document)

                # change the sequence identifier and sequence number
                document.sequence_identifier = self._sequence_identifier
                #document.sequence_number = self._sequence_number

                document.validate()
                self.producer_carriage.emit_data(data=document, **kwargs)

    def remove_duplication(self, document, original_styles, original_regions, new_style_list, new_region_list, styling_element, region_element, span_style_id, region_style_id):

        for style in enumerate(document.tt.head.styling):
            original_styles.append(style)

        # for region in enumerate(document.tt.head.layout):
        #     original_regions.append(region)

        mirror_styles = original_styles

        mirror_styles_no_id = set()

        for mirror_entry in mirror_styles:
            mirror_entry_no_id = mirror_entry.rstrip(style.id)

            mirror_styles_no_id.add(mirror_entry_no_id)

            mirror_styles_new_id = list(mirror_styles_no_id)

            for x in enumerate(mirror_styles_new_id):
                new_style = mirror_styles_new_id.append("xml:id=\"style\"" + str(x))

                for span_style in enumerate(document.tt.body):
                    div.p.span.style = new_style

                for new_styling in enumerate(mirror_styles_new_id):
                    document.tt.head.styling.add(new_styling)
