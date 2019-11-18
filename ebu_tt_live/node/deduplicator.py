from .base import AbstractCombinedNode
from ebu_tt_live.documents import EBUTT3DocumentSequence, EBUTT3Document
from ebu_tt_live.bindings.pyxb_utils import RecursiveOperation, StopBranchIteration
from ebu_tt_live.strings import DOC_RECEIVED
from ebu_tt_live.errors import SequenceNumberCollisionError, UnexpectedSequenceIdentifierError
from pyxb.binding.basis import ElementContent, complexTypeDefinition
from pyxb import BIND
from pyxb.namespace import ExpandedName
from ebu_tt_live import bindings
import logging


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')

class DeDuplicatorNode(AbstractCombinedNode):
    """
    The DeDuplicator Node addresses the issue raised, whereby after ReSequencing duplication
    of style and region elements and attributes occurs.
    """
    _sequence_identifier = None
    _expects = EBUTT3Document
    _provides = EBUTT3Document

    def __init__(self, node_id, sequence_identifier, consumer_carriage=None, \
                 producer_carriage=None):
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

                document.sequence_identifier = self._sequence_identifier

                self.remove_duplication(document=document)

                document.validate()
                self.producer_carriage.emit_data(data=document, **kwargs)

    def remove_duplication(self, document):
        old_id_dict = dict({})
        new_id_dict = dict({})
        hash_dict = dict({})

        if document.binding.head.styling is not None:
            styles = document.binding.head.styling.style
            document.binding.head.styling.style = None

            self.CollateUniqueVals(styles, old_id_dict, new_id_dict, hash_dict)
            self.AppendNewElements(styles, document.binding.head.styling.style, \
                                   old_id_dict, new_id_dict, hash_dict)

        if document.binding.head.layout is not None:
            regions = document.binding.head.layout.region
            document.binding.head.layout.region = None

            self.CollateUniqueVals(regions, old_id_dict, new_id_dict, hash_dict)
            self.AppendNewElements(regions, document.binding.head.layout.region, \
                                   old_id_dict, new_id_dict, hash_dict)


        replace_id_refs = ReplaceStylesAndRegions(document.binding, \
                                                      old_id_dict, \
                                                      new_id_dict)
        replace_id_refs.proceed()

    def CollateUniqueVals(self, element_list, old_id_dict, new_id_dict, \
                          hash_dict):
        """
        Creates a `dict()` of all unique style/region names
        """
        for value in element_list:
            #deduplicating in-line style attributes
            if value.style is not None:
                for old_id_index in range(len(value.style)):
                    old_id_ref = old_id_dict.get(value.style[old_id_index])
                    new_id_ref = new_id_dict.get(old_id_ref)

                    value.style[old_id_index] = new_id_ref

            #deduplicating elements
            if value is not None:
                unique_val = ComparableElement(value)
                # stores references of original <xml:id> to <my_hash>
                old_id_dict[value.id] = unique_val.my_hash
                # stores references of <my_hash> to element
                hash_dict[unique_val.my_hash] = value

    def AppendNewElements(self, element_list, element_to_append_to, old_id_dict, \
                          new_id_dict, hash_dict):
        """
        Replaces starting style and region elements with the unique ones identified in
        CollateUniqueVals
        """
        for hash_val, new_id in hash_dict.items():

            for old_element in element_list:
                if old_element.id is new_id.id:
                    element_to_append_to.append(new_id)

            new_id_dict[hash_val] = new_id.id

def ReplaceNone(attr_value):
    """
    If an attribute has no value, it is given non-legal character as a value, to
    prevent 'collisions'
    """
    if attr_value is None:
        return "|" # '|' is a non-legal character and this is used to prevent
                   # collisions between similar attributes
    else:
        return attr_value


class ComparableElement:
    """
    Takes all the attributes of an element and returns a hash value
    """
    def __init__(self, value):
        self.value = value

        attributeDict = value._AttributeMap.copy()
        xml_id_attr = ExpandedName('http://www.w3.org/XML/1998/namespace', 'id')
        attributeDict.pop(xml_id_attr) # This shouldn't throw an error, but if it does, something's wrong

        # sorted to make sure that for two elements with the same set of
        # attributes the values are put into the hash string in the same order
        sortedDict = sorted(list(attributeDict.items()), key=lambda t: t[0])

        concatenatedStyleString = ''
        for key,val in sortedDict:
            styleValue = ReplaceNone(val.value(value))
            concatenatedStyleString += str(styleValue) + '%'

        for key,val in list(value.wildcardAttributeMap().items()):
            namespace = ReplaceNone(key.namespaceURI())
            localName = key.localName()
            wildcardValue = ReplaceNone(val)
            concatenatedStyleString += namespace + '%' + localName + '%' + wildcardValue

        self.my_hash = hash(concatenatedStyleString)

    def __eq__(self, other):
        return other and self.my_hash == other.my_hash

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.my_hash


class ReplaceStylesAndRegions(RecursiveOperation):
    old_id_dict = None
    new_id_dict = None

    def __init__(self, root_element, old_id_dict, new_id_dict):
            super(ReplaceStylesAndRegions, self).__init__(
                root_element
            )

            self.old_id_dict = old_id_dict
            self.new_id_dict = new_id_dict

    def _is_begin_timed(self, value):
        pass

    def _before_element(self, value, element=None, parent_binding=None, **kwargs):
        pass

    def _after_element(self, value, element=None, parent_binding=None, **kwargs):
        pass

    def _process_element(self, value, element=None, parent_binding=None, **kwargs):
        """
        Replaces the style and region attributes in the rest of
        """
        # The latter part of this and the next test is to check that the instance
        # is not a styling or layout element as these can't have style attributes
        # but their style elements present themselves in exactly the same way as
        # style attributes on other elements, so we have to avoid getting confused by them
        if hasattr(value, 'style') and value.style is not None and not \
        isinstance(value, bindings.styling):
            id_to_index_dict = dict()
            # Stepping backwards to preserve hierarchy of style attributes
            for old_id_index in range(len(value.style)-1, -1, -1):
                old_id_ref = self.old_id_dict.get(value.style[old_id_index])
                new_id_ref = self.new_id_dict.get(old_id_ref)

                # Next two lines remove in-line style duplication
                if new_id_ref in id_to_index_dict:
                    del value.style[id_to_index_dict[new_id_ref]]

                id_to_index_dict[new_id_ref] = old_id_index

                value.style[old_id_index] = new_id_ref
        else:
            pass

        if hasattr(value, 'region') and value.region is not None and not \
        isinstance(value, bindings.layout):
            old_id_ref = self.old_id_dict.get(value.region)
            new_id_ref = self.new_id_dict.get(old_id_ref)

            value.region = new_id_ref
        else:
            pass

    def _process_non_element(self, value, non_element, parent_binding=None, **kwargs):
        pass
