
from ebu_tt_live.node import HandoverNode
from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.documents import EBUTT3Document, EBUTTAuthorsGroupControlRequest


class HandoverUnittests(TestCase):

    _sequence_identifier = 'test_output_sequence'
    _authors_group_identifier = 'test_group'

    def setUp(self):
        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = HandoverNode.provides()
        self.handover = HandoverNode(
            node_id='test_handover_node',
            authors_group_identifier=self._authors_group_identifier,
            sequence_identifier=self._sequence_identifier,
            producer_carriage=carriage
        )

    def _create_test_document(self, sequence_identifier, sequence_number, authors_group_identifier=None,
                              authors_group_control_token=None, authors_group_control_request=None):
        doc = MagicMock(spec=EBUTT3Document)
        doc.sequence_identifier = sequence_identifier
        doc.sequence_number = sequence_number
        doc.authors_group_identifier = authors_group_identifier
        doc.authors_group_control_token = authors_group_control_token
        doc.authors_group_control_request = authors_group_control_request

        return doc

    def test_ignored_documents(self):
        doc1 = self._create_test_document(
            sequence_identifier='seq1',
            sequence_number=1
        )
        doc2 = self._create_test_document(
            sequence_identifier='seq1',
            sequence_number=2,
            authors_group_identifier='wrong_group',
            authors_group_control_token=3
        )

        self.handover.process_document(doc1)
        self.handover.process_document(doc2)

        # Nothing is supposed to be processed when documents lack identifiers
        self.handover.producer_carriage.emit_data.assert_not_called()

    def test_switch_and_emit(self):
        doc1 = self._create_test_document(
            sequence_identifier='seq1',
            sequence_number=4,
            authors_group_identifier=self._authors_group_identifier,
            authors_group_control_token=1
        )
        doc2 = self._create_test_document(
            sequence_identifier='seq2',
            sequence_number=4,
            authors_group_identifier=self._authors_group_identifier,
            authors_group_control_token=2
        )

        self.handover.process_document(doc1)
        self.handover.process_document(doc2)

        assert self.handover.producer_carriage.emit_data.call_count, 2  # 2 documents were processed
        # First document should be doc1
        assert self.handover.producer_carriage.emit_data.call_args_list[0][1]['data'] == doc1
        # Second document should be doc2
        assert self.handover.producer_carriage.emit_data.call_args_list[1][1]['data'] == doc2
        # Sequence reassignment
        assert doc1.sequence_identifier == self._sequence_identifier
        # Sequence number reassignment
        assert doc1.sequence_number == 1
        # Same for doc2
        assert doc2.sequence_identifier == self._sequence_identifier
        assert doc2.sequence_number == 2
        # Check current tracked sequence is seq2
        assert self.handover._current_selected_input_sequence_id == 'seq2'
        # Last issued sequence number is 2
        assert self.handover._last_sequence_number == 2

    def test_kwargs_passthrough(self):
        doc1 = self._create_test_document(
            sequence_identifier='seq1',
            sequence_number=1,
            authors_group_identifier='test_group',
            authors_group_control_token=1
        )

        # This checks that arbitrary keyword arguments survive the process_document as it is a requirement
        # of the INode interface it implements.
        self.handover.process_document(document=doc1, bla=4)

        self.handover.producer_carriage.emit_data.assert_called_with(
            data=doc1,
            bla=4
        )

    def test_control_request_passthrough(self):
        message = EBUTTAuthorsGroupControlRequest(
            sequence_identifier='TestSequence',
            sender='testSender',
            recipient=[
                'rec1',
                'rec2'
            ],
            payload='This is a test request'
        )

        self.handover.process_document(document=message)

        self.handover.producer_carriage.emit_data.assert_called_with(
            data=message
        )

