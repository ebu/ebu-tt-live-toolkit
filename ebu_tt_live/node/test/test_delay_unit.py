import six
from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.node.delay import RetimingDelayNode, BufferDelayNode
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.documents import EBUTT3Document, EBUTTAuthorsGroupControlRequest


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
