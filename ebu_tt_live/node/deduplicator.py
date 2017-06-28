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
    _new_style_set = set()
    _new_region_set = set()
    _old_style_id_dict = dict({})
    _new_style_id_dict = dict({})
    _old_region_id_dict = dict({})
    _new_region_id_dict = dict({})
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
                print document.get_xml()

                document.validate()
                self.producer_carriage.emit_data(data=document, **kwargs)

    def remove_duplication(self, document):
        # print(vars(document.binding.head.styling))
        # print(dir(document.binding.head.styling))
        # print document.get_xml()
        # old_style_id_dict = dict({})
        # new_style_id_dict = dict({})
        hash_style_dict = dict({})
        new_style_list = list()

        hash_region_dict = dict({})
        new_region_list = list()

        styles = document.binding.head.styling.style
        regions = document.binding.head.layout.region

        for style in styles:
            self._original_styles.append(style)

        for value in self._original_styles:
            unique_val = ComparableStyle(value)
            self._old_style_id_dict[value.id] = unique_val.my_hash  # stores references of original <xml:id> to <my_hash>
            hash_style_dict[unique_val.my_hash] = value # stores references of <my_hash> to <tt:style>

            self._new_style_set.add(unique_val.my_hash)

        for style_hash in self._new_style_set:
            new_id = hash_style_dict.get(style_hash)
            new_style_list.append(new_id)
            self._new_style_id_dict[style_hash] = new_id.id         # stores references of <my_hash> to new <xml:id>


        for region in regions:
            self._original_regions.append(region)

        for value in self._original_regions:
            unique_val = ComparableRegion(value)
            self._old_region_id_dict[value.id] = unique_val.my_hash  # stores references of original <xml:id> to <my_hash>
            hash_region_dict[unique_val.my_hash] = value # stores references of <my_hash> to <tt:region>

            self._new_region_set.add(unique_val.my_hash)

        for region_hash in self._new_region_set:
            new_id = hash_region_dict.get(region_hash)
            new_region_list.append(new_id)
            self._new_region_id_dict[region_hash] = new_id.id

        # for x in self._original_styles:
        #     old_id_ref = old_id_dict.get(x.id)
        #     new_id_ref = new_id_dict.get(old_id_ref)
        #
        #     print(old_id_ref, new_id_ref)

        document.binding.head.styling.style = None
        for new_style in new_style_list:
            document.binding.head.styling.append(new_style)

        document.binding.head.layout.region = None
        for new_region in new_region_list:
            document.binding.head.layout.append(new_region)

        replace_id_refs = ReplaceStylesAndRegions(document.binding.body, self._old_style_id_dict, self._new_style_id_dict, self._old_region_id_dict, self._new_region_id_dict)
        replace_id_refs.proceed()


class ComparableStyle:
    def __init__(self, value):
        self.value = value

        self.my_hash = hash(value.linePadding + value.backgroundColor + value.color + value.fontFamily)

    def __eq__(self, other):
        return other and self.my_hash == other.my_hash

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.my_hash

class ComparableRegion:
    def __init__(self, value):
        self.value = value

        self.my_hash = hash(value.displayAlign + value.extent + value.origin + value.overflow + value.writingMode)

    def __eq__(self, other):
        return other and self.my_hash == other.my_hash

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.my_hash

class ReplaceStylesAndRegions(RecursiveOperation):

    def __init__(self, root_element, _old_style_id_dict, _new_style_id_dict, _old_region_id_dict, _new_region_id_dict):
            super(ReplaceStylesAndRegions, self).__init__(
                root_element,
                filter=lambda value, element: not isinstance(value, bindings.br_type)
            )
            self._old_style_id_dict = _old_style_id_dict
            self._new_style_id_dict = _new_style_id_dict
            self._old_region_id_dict = _old_region_id_dict
            self._new_region_id_dict = _new_region_id_dict

    def _is_begin_timed(self, value):
        pass

    def _before_element(self, value, element=None, parent_binding=None, **kwargs):
        pass

    def _after_element(self, value, element=None, parent_binding=None, **kwargs):
        pass

    def _process_element(self, value, element=None, parent_binding=None, **kwargs):
        if value.style is not None:
            for old_id_index in range(len(value.style)):
                old_id_ref = self._old_style_id_dict.get(value.style[old_id_index])
                new_id_ref = self._new_style_id_dict.get(old_id_ref)

                value.style[old_id_index] = new_id_ref
        else:
            pass

        if not isinstance(value, bindings.body_type) and not isinstance(value, bindings.span_type) and value.region is not None:
            old_id_ref = self._old_region_id_dict.get(value.region)
            new_id_ref = self._new_region_id_dict.get(old_id_ref)

            value.region = new_id_ref
        else:
            pass

    def _process_non_element(self, value, non_element, parent_binding=None, **kwargs):
        pass
