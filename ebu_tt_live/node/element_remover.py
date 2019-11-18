from .base import AbstractCombinedNode
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.errors import UnexpectedSequenceIdentifierError
from pyxb.binding.basis import ElementContent, \
    complexTypeDefinition, simpleTypeDefinition
import logging

log = logging.getLogger(__name__)


class ElementRemoverNode(AbstractCombinedNode):
    """
    Removes unwanted elements from a document.

    Matches elements by local names only. Restricted to
    XML elements that have bindings; non-bound elements
    are left in place.
    """

    _expects = EBUTT3Document
    _provides = EBUTT3Document

    _remove_list = []
    _sequence_identifier = None
    _last_sequence_number = None

    def __init__(self,
                 node_id,
                 sequence_identifier,
                 consumer_carriage=None,
                 producer_carriage=None,
                 remove_list=''):
        super(ElementRemoverNode, self).__init__(
            node_id=node_id,
            producer_carriage=producer_carriage,
            consumer_carriage=consumer_carriage
        )

        self._set_remove_list(remove_list)
        self._sequence_identifier = sequence_identifier
        self._last_sequence_number = 0

    def _set_remove_list(self, remove_list):
        """
        Specify the list of element local names to remove.

        The list string must be comma separated and can include
        whitespace.

        :param remove_list: element names to remove.
        """
        self._remove_list = []
        for r in remove_list.split(','):
            self._remove_list.append(r.strip())

    def process_document(self, document, **kwargs):
        if self.is_document(document):

            if document.sequence_identifier == self._sequence_identifier:
                raise UnexpectedSequenceIdentifierError()

            if self.check_if_document_seen(document=document) is True:

                self.limit_sequence_to_one(document)

                # Remove the elements we don't want
                self.remove_unwanted_elements_from_document(document)

                # Update the sequence identifier and number and emit the
                # document
                self._last_sequence_number += 1
                document.sequence_identifier = self._sequence_identifier
                document.sequence_number = self._last_sequence_number

                document.validate()
                self.producer_carriage.emit_data(
                    data=document,
                    **kwargs
                    )
            else:
                log.warning(
                    'Ignoring duplicate document: {}__{}'.format(
                        document.sequence_identifier,
                        document.sequence_number
                    )
                )
        else:
            document.sequence_identifier = self._sequence_identifier
            self.producer_carriage.emit_data(
                data=document,
                **kwargs
            )

    def remove_unwanted_elements_from_document(self, document):
        """
        Remove unwanted elements from the provided document.

        Use this method to remove elements from a document if you are not using
        concrete carriage mechanisms and want to manage document processing
        manually.

        :param SubtitleDocument document: the document whose elements are to be removed
        :return SubtitleDocument: returns the provided input document, but with removed elements.
        """
        self.remove_unwanted_elements(document.binding)
        return document

    def remove_unwanted_elements(self, element):
        """Recursive function."""
        children = []

        # We only get a meaningful list of child elements from
        # element.orderedContent() in some specific conditions!
        if not isinstance(element, list) and \
           not isinstance(element, simpleTypeDefinition) and \
           isinstance(element, complexTypeDefinition) and \
           not element._IsSimpleTypeContent():
            children = element.orderedContent()

        for item in children:
            # Some children might be NonElementContent, so check they are
            # all genuine ElementContent before testing them further.
            if isinstance(item, ElementContent):
                if item.elementDeclaration is not None:
                    local_name = item.elementDeclaration.name().localName()
                    if local_name in self._remove_list:
                        # Remove this element
                        setattr(element, local_name, None)
                    else:
                        # Recurse to the children
                        self.remove_unwanted_elements(item.value)
