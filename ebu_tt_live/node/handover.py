
from .switcher import SwitcherNode
from ebu_tt_live.documents import EBUTT3Document


class HandoverNode(SwitcherNode):
    """
    The handover node implements the functionality described in EBU-3370. It is a specialised case
    of the switching node basing its decisions on the handover-related attributes on the document root element and
    on its previous decisions.
    """

    _expects = EBUTT3Document
    _provides = EBUTT3Document
    _sequence_identifier = None
    _authors_group_identifier = None
    _current_token = None
    _current_selected_input_sequence_id = None
    _last_sequence_number = None

    def __init__(self, node_id, authors_group_identifier, sequence_identifier, consumer_carriage=None, producer_carriage=None, **kwargs):
        super(HandoverNode, self).__init__(
            node_id=node_id,
            consumer_carriage=consumer_carriage,
            producer_carriage=producer_carriage,
            **kwargs
        )
        self._authors_group_identifier = authors_group_identifier
        self._sequence_identifier = sequence_identifier
        self._current_sequence_id = None
        self._last_sequence_number = 0

    def process_document(self, document, **kwargs):
        """
        The specified functionality is met by keeping the following priorities in mind when processing an
        incoming document:

          - If sequenceIdentifier matches the one selected the document should be emitted
          - If sequenceIdentifier does not match the one selected or one is not selected

            - If authorsGroupIdentifier is not matching the one set in the initializer ignore the document
            - If authorsGroupIdentifier is the right one

              - If the token is higher than our current one or one is not set the document should be emitted
              - If token is lower than the our current one the document should be ignored

          - If the document should be emitted

            - Set/update selected sequenceIdentifier from the one in the document
            - Set/update authorsGroupControlToken if specified
            - Emit document

        :param document:
        :param kwargs:

        """
        emit = False

        if document.sequence_identifier == self._current_selected_input_sequence_id:
            # Maintain selection
            emit = True
        else:
            if document.authors_group_identifier == self._authors_group_identifier:
                if self._current_token is None or self._current_token < document.authors_group_control_token:
                    # Switch input
                    self._current_selected_input_sequence_id = document.sequence_identifier
                    emit = True

        if emit is True:
            if document.authors_group_control_token is not None:
                # Update token
                self._current_token = document.authors_group_control_token  # So are we going to error here?

            self._last_sequence_number += 1
            document.sequence_number = self._last_sequence_number
            self.producer_carriage.emit_data(
                data=document,
                **kwargs
            )
