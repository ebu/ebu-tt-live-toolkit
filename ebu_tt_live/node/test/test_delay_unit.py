import six
from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.node.delay import RetimingDelayNode, BufferDelayNode
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.documents import EBUTT3Document, EBUTTAuthorsGroupControlRequest
from ebu_tt_live.errors import UnexpectedSequenceIdentifierError
from ebu_tt_live.bindings._ebuttm import documentMetadata, headMetadata_type


class TestRetimingDelayNode(TestCase):

    def setUp(self):
        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = EBUTT3Document
        delay = 2
        document_sequence = 'TestSequence'
        self.retiming_delay_node = RetimingDelayNode(
            node_id='delay_node',
            fixed_delay=delay,
            document_sequence=document_sequence,
            producer_carriage=carriage
        )

    def test_process_document(self):
        document = MagicMock(spec=EBUTT3Document)
        self.retiming_delay_node.process_document(document)
        self.retiming_delay_node.producer_carriage.emit_data.assert_called_with(data=document)

    def test_control_request_passthrough(self):
        # It should pass through
        message = EBUTTAuthorsGroupControlRequest(
            sequence_identifier='TestSequence',
            sender='testSender',
            recipient=[
                'rec1',
                'rec2'
            ],
            payload='This is a test request'
        )

        self.retiming_delay_node.process_document(document=message)

        self.retiming_delay_node.producer_carriage.emit_data.assert_called_with(
            data=message
        )

    def test_process_two_documents_ignore_second_sequence_id(self):

        first_sequence = MagicMock(spec=EBUTT3Document)
        first_sequence.sequence_identifier = 'TestSequence1'

        second_sequence = MagicMock(spec=EBUTT3Document)
        second_sequence.sequence_identifier = 'TestSequence2'

        self.retiming_delay_node.process_document(document=first_sequence)
        self.retiming_delay_node.producer_carriage.emit_data.assert_called_with(
            data=first_sequence
        )

        with self.assertRaises(UnexpectedSequenceIdentifierError) as context:
            self.retiming_delay_node.process_document(document=second_sequence)

        self.assertTrue('Rejecting new sequence identifier' in context.exception.message)

    def test_if_metadata_applied_processing_is_defined(self):

        def test(data):
            self.assertIsInstance(data.binding.head.metadata, headMetadata_type)
            self.assertIsInstance(data.binding.head.metadata.documentMetadata, documentMetadata)
            self.assertEqual(data.binding.head.metadata.documentMetadata.appliedProcessing, documentMetadata().appliedProcessing)

        self.retiming_delay_node.producer_carriage.emit_data = test

        document = MagicMock(spec=EBUTT3Document)

        document.binding.head.metadata = None

        self.retiming_delay_node.process_document(document)

class TestBufferDelayNode(TestCase):

    def setUp(self):
        self.delay = 2
        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = six.text_type

        self.buffer_delay_node = BufferDelayNode(
            node_id='delay_node',
            producer_carriage=carriage,
            fixed_delay=self.delay
        )

    def test_process_document(self):
        document = MagicMock(spec=EBUTT3Document)
        self.buffer_delay_node.process_document(document)
        self.buffer_delay_node.producer_carriage.emit_data.assert_called_with(
            data=document, delay=self.delay
        )

    def test_control_request_passthrough(self):
        # It should pass through
        message = EBUTTAuthorsGroupControlRequest(
            sequence_identifier='TestSequence',
            sender='testSender',
            recipient=[
                'rec1',
                'rec2'
            ],
            payload='This is a test request'
        )

        self.buffer_delay_node.process_document(document=message)

        self.buffer_delay_node.producer_carriage.emit_data.assert_called_with(
            data=message, delay=self.delay
        )
