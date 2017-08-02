from ebu_tt_live.documents import EBUTT3Document, EBUTTDDocument, EBUTTAuthorsGroupControlRequest
from ebu_tt_live.node.deduplicator import DeDuplicatorNode
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.errors import UnexpectedSequenceIdentifierError
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttm as metadata
from ebu_tt_live.bindings import _ebuttdt as datatypes
from datetime import timedelta
from unittest import TestCase
from pyxb import BIND
from mock import MagicMock


class DeDuplicatorUnitTest(TestCase):

    def _create_test_document(self):
        doc = EBUTT3Document(
            time_base='clock',
            clock_mode='local',
            lang='en-GB',
            sequence_identifier='testSequenceDeDuplicator01',
            sequence_number='1'
        )
        head_elem = bindings.head_type(
            metadata.headMetadata_type(
                metadata.documentMetadata()
            ),
            bindings.styling(
                bindings.style_type(
                    id='SEQ58.defaultStyle1',
                    linePadding='0.5c',
                    backgroundColor='rgb(0, 0, 0)',
                    color='rgb(255, 255, 255)',
                    fontFamily='sansSerif'
                ),
                bindings.style_type(
                    id='SEQ59.defaultStyle1',
                    linePadding='0.5c',
                    backgroundColor='rgb(0, 0, 0)',
                    color='rgb(255, 255, 255)',
                    fontFamily='sansSerif'
                ),
                bindings.style_type(
                    id='SEQ60.defaultStyle1',
                    linePadding='0.5c',
                    backgroundColor='rgb(0, 0, 0)',
                    color='rgb(255, 255, 255)',
                    fontFamily='sansSerif'
                )
            ),
            bindings.layout(
                bindings.region_type(
                    id='SEQ58.bottomRegion',
                    displayAlign='after',
                    extent='71.25% 24%',
                    origin='14.375% 60%',
                    overflow='visible',
                    writingMode='lrtb'
                ),
                bindings.region_type(
                    id='SEQ59.bottomRegion',
                    displayAlign='after',
                    extent='71.25% 24%',
                    origin='14.375% 60%',
                    overflow='visible',
                    writingMode='lrtb'
                ),
                bindings.region_type(
                    id='SEQ560.bottomRegion',
                    displayAlign='after',
                    extent='71.25% 24%',
                    origin='14.375% 60%',
                    overflow='visible',
                    writingMode='lrtb'
                )
            )
        )
        body_elem = bindings.body_type(
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Multiply your anger by about a',
                        style=['SEQ58.defaultStyle1']
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'hundred, Kate, that\'s how much he',
                        style=['SEQ58.defaultStyle1']
                    ),
                    id='SEQ58.ID001.1'
                ),
                region='SEQ58.bottomRegion'
            ),
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'thinks he loves you.',
                        style=['SEQ59.defaultStyle1']
                    ),
                    id='SEQ59.ID001.1'
                ),
                region='SEQ59.bottomRegion'
            ),
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Multiply your anger by about a',
                        style=['SEQ60.defaultStyle1']
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'hundred, Kate, that\'s how much he',
                        style=['SEQ60.defaultStyle1']
                    ),
                    id='SEQ60.ID001.1'
                ),
                region='SEQ60.bottomRegion'
            )
        )

        doc.binding.head = head_elem
        doc.binding.body = body_elem
        doc.validate()
        raw_xml = doc.get_xml()
        doc = EBUTT3Document.create_from_xml(raw_xml)
        return doc

    def setUp(self):
        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = EBUTT3Document

        self.deduplicator = DeDuplicatorNode(
            node_id='testDeDuplicatorNode',
            sequence_identifier='testDeDuplicated1',
            producer_carriage=carriage
        )

    def test_basic_operation(self):
        doc = self._create_test_document()

        self.deduplicator.process_document(document=doc)
        self.deduplicator.producer_carriage.emit_data.assert_called_once()
        self.assertIsInstance(
            self.encoder.producer_carriage.emit_data.call_args[1]['data'],
            EBUTT3Document
        )
