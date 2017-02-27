from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.node.distributing import DistributingNode
import six


class TestDistributingNode(TestCase):

    def test_process_document(self):
        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = six.text_type
        reference_clock = MagicMock()
        node = DistributingNode(
            node_id='distributing_node',
            producer_carriage=carriage,
            reference_clock=reference_clock
        )
        document = MagicMock(spec=EBUTT3Document)
        node.process_document(document)
        carriage.emit_data.assert_called_with(data=document.get_xml())

    def test_process_document_raw_xml(self):
        # In this test there is a raw_xml kwarg passed in. If that parameter is set it is used instead of
        # document.get_xml()
        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = six.text_type
        reference_clock = MagicMock()
        node = DistributingNode(
            node_id='distributing_node',
            producer_carriage=carriage,
            reference_clock=reference_clock
        )
        document = MagicMock(spec=EBUTT3Document)
        raw_xml = MagicMock(spec=six.text_type)
        node.process_document(document=document, raw_xml=raw_xml)
        carriage.emit_data.assert_called_with(data=raw_xml)

    def test_check_document_buffer_overflow(self):
        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = six.text_type
        reference_clock = MagicMock()
        node = DistributingNode(
            node_id='distributing_node',
            producer_carriage=carriage,
            reference_clock=reference_clock
        )
        seq_id = 'testSequence01'
        for item in xrange(100):
            node.check_document(sequence_identifier=seq_id, sequence_number=item)

        # It should still be here
        self.assertFalse(node.check_document(sequence_identifier=seq_id, sequence_number=0))
        # the 101 should push the first element (0) out of the fifo.
        node.check_document(sequence_identifier=seq_id, sequence_number=101)
        self.assertTrue(node.check_document(sequence_identifier=seq_id, sequence_number=0))
