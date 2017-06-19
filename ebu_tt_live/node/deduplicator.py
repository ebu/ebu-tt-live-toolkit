from .base import AbstractCombinedNode
from ebu_tt_live.documents import EBUTT3DocumentSequence, EBUTT3Document
from ebu_tt_live.bindings import _ebuttm as metadata
from ebu_tt_live.bindings.pyxb_utils import RecursiveOperation, StopBranchIteration
from ebu_tt_live.strings import DOC_RECEIVED
from ebu_tt_live.errors import SequenceNumberCollisionError, UnexpectedSequenceIdentifierError
from pyxb.binding.basis import NonElementContent, ElementContent
from pyxb import BIND
from ebu_tt_live import bindings
import logging


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class DeDuplicatorNode(AbstractCombinedNode, RecursiveOperation):
    _original_styles = []
    _original_regions = []
    _mirror_styles_no_id = []
    _new_style_list = []
    _new_region_list = []
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

                self.remove_duplication(document=document)

                document.validate()
                self.producer_carriage.emit_data(data=document, **kwargs)

    def remove_duplication(self, document):
        # print(vars(document.binding.head.styling))
        # print(dir(document.binding.head.styling))
        # print document.get_xml()

        styling_list = document.binding.head.styling.orderedContent()
            for style in styling_list:
                self._original_styles.append(style)

            root_of_search = document.binding.body.orderedContent()
            for body_content in root_of_search:
                self._body_content_list.append(body_content)

            mirror_styles = self._original_styles
            self._mirror_styles_no_id = set()

            for span_search in self._body_content_list:

                for mirror_entry in mirror_styles:
                    mirror_entry.id = None
                    mirror_entry_no_id = mirror_entry

                    self._mirror_styles_no_id.add(mirror_entry_no_id)

                    mirror_styles_new_id = list(self._mirror_styles_no_id)

                    for new_style in mirror_styles_new_id:
                        for x in range(len(mirror_styles_new_id)):
                            new_id = "style" + str(x)
                        new_style.id = new_id

                span_search.span = None
                span_search.span = new_id

            document.binding.head.styling.style = None
            for y in mirror_styles_new_id:
                document.binding.head.styling.append(mirror_styles_new_id)
