from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.node.distributing import DistributingNode


class TestDistributingNode(TestCase):

    def test_process_document(self):
        carriage = MagicMock()
        reference_clock = MagicMock()
        node = DistributingNode('distributing_node', carriage, reference_clock)
        document = MagicMock()
        node.process_document(document)
        carriage.emit_document.assert_called_with(document)
