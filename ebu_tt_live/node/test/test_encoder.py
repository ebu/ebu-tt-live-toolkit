from ebu_tt_live.documents import EBUTT3Document, EBUTTDDocument, EBUTTAuthorsGroupControlRequest
from ebu_tt_live.node.encoder import EBUTTDEncoder
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live import bindings
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttm as metadata
from ebu_tt_live.bindings import _ebuttdt as datatypes
from datetime import timedelta
from unittest import TestCase
from pyxb import BIND
from mock import MagicMock


class TestEBUTTDEncoderSuccess(TestCase):

    def _create_test_document(self):
        doc = EBUTT3Document(
            time_base='clock',
            clock_mode='local',
            lang='en-GB',
            sequence_identifier='testSequenceEncoder01',
            sequence_number='1'
        )

        head_elem = bindings.head_type(
            metadata.headMetadata_type(
                metadata.documentMetadata()
            ),
            bindings.styling(
                bindings.style_type(
                    id='style1',
                    fontSize='12px'
                ),
                bindings.style_type(
                    id='style2',
                    fontSize='15px'
                ),
                bindings.style_type(
                    id='style3',
                    color='red',
                    fontSize='12px'
                ),
                bindings.style_type(
                    id='style4',
                    backgroundColor='blue'
                )
            ),
            bindings.layout(
                bindings.region_type(
                    id='region1',
                    origin='200px 450px',
                    extent='300px 150px',
                    style=['style3']
                )
            )
        )

        body_elem = bindings.body_type(
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Some example text...',
                        begin=datatypes.LimitedClockTimingType(timedelta(hours=11, minutes=32, seconds=1)),
                        end=datatypes.LimitedClockTimingType(timedelta(hours=11, minutes=32, seconds=2)),
                        style=['style4'],
                        id='span1'
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'And another line',
                        begin=datatypes.LimitedClockTimingType(timedelta(hours=11, minutes=32, seconds=3)),
                        end=datatypes.LimitedClockTimingType(timedelta(hours=11, minutes=32, seconds=4)),
                        id='span2'
                    ),
                    id='ID005',
                ),
                style=['style1'],
                region='region1'
            ),
            begin=datatypes.LimitedClockTimingType(timedelta(hours=11, minutes=32, seconds=.5)),
            dur=datatypes.LimitedClockTimingType(timedelta(hours=11, minutes=32, seconds=5)),
            style=['style2']
        )

        doc.binding.head = head_elem
        doc.binding.body = body_elem
        doc.binding.extent = '800px 600px'
        doc.validate()
        raw_xml = doc.get_xml()
        doc = EBUTT3Document.create_from_xml(raw_xml)
        return doc

    def setUp(self):
        carriage = MagicMock(spec=IProducerCarriage)
        carriage.expects.return_value = EBUTTDDocument

        self.encoder = EBUTTDEncoder(
            node_id='testEncoder',
            producer_carriage=carriage,
            media_time_zero=timedelta(hours=11, minutes=32)
        )

    def test_basic_operation(self):
        doc = self._create_test_document()

        self.encoder.process_document(document=doc)
        self.encoder.producer_carriage.emit_data.assert_called_once()
        self.assertIsInstance(
            self.encoder.producer_carriage.emit_data.call_args[1]['data'],
            EBUTTDDocument
        )

    def test_control_request(self):
        # The message should not pass through the encoder
        message = EBUTTAuthorsGroupControlRequest(
            sender='sender',
            recipient=['one', 'two'],
            payload='Test payload'
        )

        self.encoder.process_document(document=message)

        self.encoder.producer_carriage.emit_data.assert_not_called()