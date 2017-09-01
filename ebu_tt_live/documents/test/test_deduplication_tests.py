import six
from unittest import TestCase
from mock import MagicMock
import os
from ebu_tt_live import bindings
from ebu_tt_live.node.deduplicator import DeDuplicatorNode, ReplaceStylesAndRegions, ReplaceNone
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.bindings import style_type, region_type, div_type, p_type, span_type, br_type, ebuttdt


class TestDeDuplicator(TestCase):

# CollateUniqueVals
# to be given a list of elements, which it then performs in-line deduplication
# and then produces two dicts, one with old ids and hashes, the other with hashes
# and unique ids
    def setUp(self):
        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = EBUTT3Document
        document_sequence = 'TestSequence'
        self.deduplicatorNode = DeDuplicatorNode(
            node_id = 'deduplicator_node',
            sequence_identifier = document_sequence,
            producer_carriage = carriage
        )

    def test_process_document(self):
        document = MagicMock(spec=EBUTT3Document)
        self.deduplicatorNode.process_document(document)
        self.deduplicatorNode.producer_carriage.emit_data.assert_called_with(data=document)

    # def test_remove_duplication(self):
    #     document = MagicMock(spec=EBUTT3Document)
    #     self.deduplicatorNode.remove_duplication(document)
    #     self.deduplicatorNode.remove_duplication.assertIs(document=document)

    def test_collate_unique_vals(self):
        document = MagicMock(spec=EBUTT3Document)

    def test_append_new_elements(self):
        old_id_dict = dict({})
        new_id_dict = dict({})
        hash_dict = dict({})

        test_style1 = style_type(
            direction='ltr',
            fontSize='1c 2c',
            fontFamily='Serif',
            lineHeight='normal',
            fontStyle='normal',
            fontWeight='normal',
            backgroundColor='rgb(0, 0, 0)',
            color='rgb(0, 255, 255)'
            )

        test_style2 = style_type(
            id='TSID2',
            direction='ltr',
            fontSize='1c 2c',
            fontFamily='Serif',
            lineHeight='normal',
            fontStyle='normal',
            fontWeight='normal',
            backgroundColor='rgb(0, 0, 0)',
            color='rgb(255, 255, 255)'
            )

        test_styles = [test_style1, test_style2]
        test_styles_blank = []

        self.deduplicatorNode.CollateUniqueVals(test_styles, old_id_dict, new_id_dict, hash_dict)
        self.deduplicatorNode.AppendNewElements(test_styles, test_styles_blank, old_id_dict, new_id_dict, hash_dict)

        # assert len(test_styles_blank) is 1

        # for ts in test_styles_blank:
        #     assert ts.id is not None

# ReplaceNone
# Passed attributes - where an attribute has no value, it is replaced with the
# non-legal character; if it has a value, it is returned


# ReplaceStylesAndRegions
# if I need to write these tests...passes on isbegintimed, beforeelement,
# afterelement and processnonelement
#
# for processelement to be given a document with style and region attributes
# that will be replaced with the unique ones found in new_id_dict, while also
# replacing/removing in-line styles while maintaining the hierarchy they were
# declared
