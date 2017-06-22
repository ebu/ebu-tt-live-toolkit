from .base import AbstractCombinedNode
from ebu_tt_live.documents import EBUTT3DocumentSequence, EBUTT3Document
# from ebu_tt_live.bindings import _ebuttm as metadata
from ebu_tt_live.bindings.pyxb_utils import RecursiveOperation, StopBranchIteration
from ebu_tt_live.strings import DOC_RECEIVED
from ebu_tt_live.errors import SequenceNumberCollisionError, UnexpectedSequenceIdentifierError
# from pyxb.binding.basis import NonElementContent, ElementContent
from pyxb import BIND
from ebu_tt_live import bindings
import logging


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class DeDuplicatorNode(AbstractCombinedNode):
    _original_styles = []
    _original_regions = []
    _mirror_list = []
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
                self.comparison_method(self._original_styles)

                document.validate()
                self.producer_carriage.emit_data(data=document, **kwargs)

    def remove_duplication(self, document):
        # print(vars(document.binding.head.styling))
        # print(dir(document.binding.head.styling))
        # print document.get_xml()

        styles = document.binding.head.styling.style
        # print styling_list
        for style in styles:
            self._original_styles.append(style)

        # for region in enumerate(document.tt.head.layout):
        #     original_regions.append(region)

    def comparison_method(self, something_to_compare):
        self._mirror_list = something_to_compare

        for value in something_to_compare:
            print value.color
            for value_to_compare in self._mirror_list
                for attr in vars(value):
                    print attr
                    if getattr(value, attr) is not getattr(value_to_compare, attr):
                        return False
                    else:
                        pass




        # self._mirror_styles_no_id = set()
        #
        # for mirror_entry in mirror_styles:
        #     #old_id_copy = mirror_entry.id
        #     mirror_entry.id = None
        #     mirror_entry_no_id = mirror_entry
        #
        #     self._mirror_styles_no_id.add(mirror_entry_no_id)#, old_id_copy)
        #
        #     mirror_styles_new_id = list(self._mirror_styles_no_id)
        #
        #     for new_style in mirror_styles_new_id:
        #         for x in range(len(mirror_styles_new_id)):
        #             new_id = "style" + str(x)
        #         print new_style.id
        #         new_style.id = new_id
        #
        # print mirror_styles_new_id

        # document.binding.head.styling.style = None
        # document.binding.head.styling = mirror_styles_new_id

class ReplaceStylesAndRegions(RecursiveOperation):
    # _path_found = False
    # _timed_element_stack = None
    #
    # def __init__(self, root_element):
    #     self._timed_element_stack = []
    #     super(r, self).__init__(
    #         root_element,
    #     )

    def _is_begin_timed(self, value):
        pass

    def _before_element(self, value, element=None, parent_binding=None, **kwargs):
        pass

    def _after_element(self, value, element=None, parent_binding=None, **kwargs):
        pass

    def _process_element(self, value, element=None, parent_binding=None, **kwargs):
        if value.style and value.region is not None:
            for x in self._original_styles:
                if value.style == x.id:
                    for y in mirror_styles_new_id:
                        if x == mirror_styles_new_id[1]:
                            value.style = mirror_styles_new_id[0].id


    def _process_non_element(self, value, non_element, parent_binding=None, **kwargs):
        pass

    # @property
    # def path_found(self):
    #     return self._path_found
