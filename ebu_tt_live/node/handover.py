
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

          - If this is a new sequence_identifier+sequence_number pair and
            authorsGroupIdentifier+authorsGroupControlToken are defined and authorsGroupIdentifier matches the
            configuration

            - If sequenceIdentifier matches the one selected the document should be emitted
            - If sequenceIdentifier does not match the one selected or one is not selected

              - If the token is higher than our current one or one is not set the document should be emitted
              - If token is lower than the our current one or missing the document should be ignored

            - If the document should be emitted

              - Set/update current sequenceIdentifier in the node from the one in the document
              - Set/update current authorsGroupControlToken in the node
              - Reassign document to output sequenceIdentifier
              - Assign new sequenceNumber to document
              - Emit document


        :param document:
        :param kwargs:

        """
        emit = False

        if self.is_document(document):
            if self.check_if_document_seen(document=document) is True \
                    and document.authors_group_identifier == self._authors_group_identifier \
                    and document.authors_group_control_token is not None:
                if self._current_token is None or self._current_token < document.authors_group_control_token:
                    # Switch input
                    self._current_selected_input_sequence_id = document.sequence_identifier
                    emit = True
                elif self._current_selected_input_sequence_id == document.sequence_identifier:
                    emit = True

            if emit is True:
                # Update token
                self._current_token = document.authors_group_control_token  # So are we going to error here?
                self._last_sequence_number += 1

                document.sequence_identifier = self._sequence_identifier
                document.sequence_number = self._last_sequence_number
                self.producer_carriage.emit_data(
                    data=document,
                    **kwargs
                )
        else:
            document.sequence_identifier = self._sequence_identifier
            self.producer_carriage.emit_data(
                data=document,
                **kwargs
            )
