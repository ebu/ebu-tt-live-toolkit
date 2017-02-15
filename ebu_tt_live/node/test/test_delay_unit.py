import six
from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.node.delay import RetimingDelayNode, BufferDelayNode
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.documents import EBUTT3Document


class TestRetimingDelayNode(TestCase):

    def test_process_document(self):

        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = EBUTT3Document
        reference_clock = MagicMock()
        delay = 2
        document_sequence = 'TestSequence'
        node = RetimingDelayNode('delay_node', carriage, reference_clock, delay, document_sequence)
        document = MagicMock(spec=EBUTT3Document)
        node.process_document(document)
        carriage.emit_data.assert_called_with(data=document)


class TestBufferDelayNode(TestCase):

    def test_process_document(self):

        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = six.text_type
        reference_clock = MagicMock()
        delay = 2
        node = BufferDelayNode('delay_node', carriage, reference_clock, delay)
        document = MagicMock(spec=EBUTT3Document)
        node.process_document(document)
        carriage.emit_data.assert_called_with(data=document, delay=delay)
