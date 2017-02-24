from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.node.distributing import DistributingNode
import six


class TestDistributingNode(TestCase):

    def test_process_document(self):
        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = EBUTT3Document
        reference_clock = MagicMock()
        node = DistributingNode(
            node_id='distributing_node',
            producer_carriage=carriage,
            reference_clock=reference_clock
        )
        document = MagicMock(spec=EBUTT3Document)
        node.process_document(document)
        carriage.emit_data.assert_called_with(data=document)
