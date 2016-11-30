from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.node.delay import RetimingDelayNode, BufferDelayNode


class TestRetimingDelayNode(TestCase):

    def test_process_document(self):

        carriage = MagicMock()
        reference_clock = MagicMock()
        delay = 2
        document_sequence = 'TestSequence'
        node = RetimingDelayNode('delay_node', carriage, reference_clock, delay, document_sequence)
        document = MagicMock()
        node.process_document(document)
        carriage.emit_document.assert_called_with(document)


class TestBufferDelayNode(TestCase):

    def test_process_document(self):

        carriage = MagicMock()
        reference_clock = MagicMock()
        delay = 2
        document_sequence = 'TestSequence'
        node = BufferDelayNode('delay_node', carriage, reference_clock, delay, document_sequence)
        document = MagicMock()
        node.process_document(document)
        carriage.emit_document.assert_called_with(document, delay=delay)
