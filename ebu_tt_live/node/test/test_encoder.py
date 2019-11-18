from ebu_tt_live.documents import EBUTT3Document, EBUTTDDocument, \
    EBUTTAuthorsGroupControlRequest
from ebu_tt_live.node.encoder import EBUTTDEncoder
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.errors import UnexpectedSequenceIdentifierError
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttm as metadata
from ebu_tt_live.bindings import _ebuttdt as datatypes
from datetime import timedelta
from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.project import description, name, version


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
                        begin=datatypes.LimitedClockTimingType(
                            timedelta(hours=11, minutes=32, seconds=1)),
                        end=datatypes.LimitedClockTimingType(timedelta(
                            hours=11, minutes=32, seconds=2)),
                        style=['style4'],
                        id='span1'
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'And another line',
                        begin=datatypes.LimitedClockTimingType(
                            timedelta(hours=11, minutes=32, seconds=3)),
                        end=datatypes.LimitedClockTimingType(
                            timedelta(hours=11, minutes=32, seconds=4)),
                        id='span2'
                    ),
                    id='ID005',
                ),
                style=['style1'],
                region='region1'
            ),
            begin=datatypes.LimitedClockTimingType(
                timedelta(hours=11, minutes=32, seconds=.5)),
            dur=datatypes.LimitedClockTimingType(
                timedelta(hours=11, minutes=32, seconds=5)),
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

        # first encoder does not calculate ittp:activeArea
        self.encoder = EBUTTDEncoder(
            node_id='testEncoder',
            producer_carriage=carriage,
            media_time_zero=timedelta(hours=11, minutes=32)
        )

        # seconds encoder does  calculate ittp:activeArea
        self.encoder2 = EBUTTDEncoder(
            node_id='testEncoder',
            producer_carriage=carriage,
            media_time_zero=timedelta(hours=11, minutes=32),
            calculate_active_area=True
        )

    def test_process_two_documents_ignore_second_sequence_id(self):

        first_sequence = self._create_test_document()
        first_sequence.sequence_identifier = 'TestSequence1'

        second_sequence = self._create_test_document()
        second_sequence.sequence_identifier = 'TestSequence2'

        self.encoder.process_document(document=first_sequence)
        self.encoder.producer_carriage.emit_data.assert_called_once()

        with self.assertRaises(UnexpectedSequenceIdentifierError) as context:
            self.encoder.process_document(document=second_sequence)

        self.assertTrue(
            'Rejecting new sequence identifier' in context.exception.args[0])

    def test_basic_operation(self):
        doc = self._create_test_document()

        self.encoder.process_document(document=doc)
        self.encoder.producer_carriage.emit_data.assert_called_once()
        output_doc = \
            self.encoder.producer_carriage.emit_data.call_args[1]['data']
        self.assertIsInstance(output_doc, EBUTTDDocument)
        self.assertIsNone(output_doc.binding.activeArea)

    def test_calculate_active_area_one_region(self):
        doc = self._create_test_document()

        self.encoder2.process_document(document=doc)
        self.encoder2.producer_carriage.emit_data.assert_called_once()
        output_doc = \
            self.encoder2.producer_carriage.emit_data.call_args[1]['data']
        self.assertIsInstance(output_doc, EBUTTDDocument)
        self.assertIsNotNone(output_doc.binding.activeArea)
        self.assertEqual(
            output_doc.binding.activeArea.xsdLiteral(),
            '25.0% 75.0% 37.5% 25.0%')

    def test_calculate_active_area_two_regions_one_unreferenced(self):
        doc = self._create_test_document()

        # Add a region but do not reference it - this should not affect
        # the calculated activeArea, because the added region is never
        # active.
        doc.binding.head.layout.region.append(
            bindings.region_type(
                id='region2',  # Deliberately not referenced
                origin='100px 450px',
                extent='300px 200px',
                style=['style3']
            )
        )

        self.encoder2.process_document(document=doc)
        self.encoder2.producer_carriage.emit_data.assert_called_once()
        output_doc = \
            self.encoder2.producer_carriage.emit_data.call_args[1]['data']
        self.assertIsInstance(output_doc, EBUTTDDocument)
        self.assertIsNotNone(output_doc.binding.activeArea)
        self.assertEqual(
            output_doc.binding.activeArea.xsdLiteral(),
            '25.0% 75.0% 37.5% 25.0%')

    def test_calculate_active_area_two_regions_both_unreferenced(self):
        doc = self._create_test_document()

        # Add a region and reference it - this should affect the calculated
        # activeArea, making it bigger.
        doc.binding.head.layout.region.append(
            bindings.region_type(
                id='region2',  # Deliberately not referenced
                origin='100px 450px',
                extent='300px 200px',
                style=['style3']
            )
        )
        doc.binding.body.div.append(
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type('some more text'),
                    id='ID006'
                ),
                region='region2',
                begin=datatypes.LimitedClockTimingType(
                    timedelta(hours=11, minutes=32, seconds=4)),
                end=datatypes.LimitedClockTimingType(
                    timedelta(hours=11, minutes=32, seconds=5))
            )
        )

        self.encoder2.process_document(document=doc)
        self.encoder2.producer_carriage.emit_data.assert_called_once()
        output_doc = \
            self.encoder2.producer_carriage.emit_data.call_args[1]['data']
        self.assertIsInstance(output_doc, EBUTTDDocument)
        self.assertIsNotNone(output_doc.binding.activeArea)
        self.assertEqual(
            output_doc.binding.activeArea.xsdLiteral(),
            '12.5% 75.0% 50.0% 33.33%')

    def test_metadata(self):
        doc = self._create_test_document()

        self.encoder.process_document(document=doc)
        self.encoder.producer_carriage.emit_data.assert_called_once()
        output_doc = \
            self.encoder.producer_carriage.emit_data.call_args[1]['data']
        self.assertIsInstance(output_doc, EBUTTDDocument)

        # Check documentConformsToStandard
        conforms_to_standard = \
            output_doc.binding.head.metadata.documentMetadata.conformsToStandard
        self.assertEqual(len(conforms_to_standard), 2)
        self.assertIn('urn:ebu:tt:distribution:2018-04', conforms_to_standard)
        self.assertIn('http://www.w3.org/ns/ttml/profile/imsc1/text', conforms_to_standard)

        # Check documentOriginatingSystem
        expected_originating_system = name + '.' + version + \
            '.EBUTT3EBUTTDConverter'
        self.assertEqual(
            output_doc.binding.head.metadata.documentMetadata.documentOriginatingSystem,
            expected_originating_system
        )

    def test_control_request(self):
        # The message should not pass through the encoder
        message = EBUTTAuthorsGroupControlRequest(
            sequence_identifier='TestSequence',
            sender='sender',
            recipient=['one', 'two'],
            payload='Test payload'
        )

        self.encoder.process_document(document=message)

        self.encoder.producer_carriage.emit_data.assert_not_called()
