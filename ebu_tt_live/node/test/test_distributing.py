from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.documents import EBUTT3Document, EBUTTAuthorsGroupControlRequest
from ebu_tt_live.node.distributing import DistributingNode
import six


class TestDistributingNode(TestCase):

    def setUp(self):
        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = six.text_type
        reference_clock = MagicMock()
        self.distributing_node = DistributingNode(
            node_id='distributing_node',
            producer_carriage=carriage,
            reference_clock=reference_clock
        )

    def test_process_document(self):

        document = MagicMock(spec=EBUTT3Document)
        self.distributing_node.process_document(document)
        self.distributing_node.producer_carriage.emit_data.assert_called_with(
            data=document.get_xml(),
            sequence_identifier=document.sequence_identifier,
            sequence_number=document.sequence_number,
            time_base=document.time_base,
            availability_time=document.availability_time
        )

    def test_process_document_raw_xml(self):
        # In this test there is a raw_xml kwarg passed in. If that parameter is set it is used instead of
        # document.get_xml()
        document = MagicMock(spec=EBUTT3Document)
        raw_xml = MagicMock(spec=six.text_type)
        self.distributing_node.process_document(document=document, raw_xml=raw_xml)
        self.distributing_node.producer_carriage.emit_data.assert_called_with(
            data=raw_xml,
            sequence_identifier=document.sequence_identifier,
            sequence_number=document.sequence_number,
            time_base=document.time_base,
            availability_time=document.availability_time
        )

    def test_check_document_buffer_overflow(self):
        seq_id = 'testSequence01'
        for item in xrange(100):
            self.distributing_node.check_if_document_seen(
                sequence_identifier=seq_id,
                sequence_number=item
            )

        # It should still be here
        self.assertFalse(
            self.distributing_node.check_if_document_seen(sequence_identifier=seq_id, sequence_number=0)
        )
        # the 101 should push the first element (0) out of the fifo.
        self.distributing_node.check_if_document_seen(sequence_identifier=seq_id, sequence_number=101)
        self.assertTrue(
            self.distributing_node.check_if_document_seen(
                sequence_identifier=seq_id,
                sequence_number=0
            )
        )

    def test_control_request(self):
        # It should propagate messages

        message = MagicMock(spec=EBUTTAuthorsGroupControlRequest)

        self.distributing_node.process_document(document=message)

        self.distributing_node.producer_carriage.emit_data.assert_called_with(
            data=message.get_xml(),
            sequence_identifier=message.sequence_identifier,
            availability_time=message.availability_time
        )
