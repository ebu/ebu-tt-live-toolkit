
from ebu_tt_live.documents import EBUTT3Document, EBUTTAuthorsGroupControlRequest, EBUTT3DocumentSequence
from ebu_tt_live.node import SimpleConsumer
from ebu_tt_live.carriage import IConsumerCarriage
from ebu_tt_live.errors import UnexpectedSequenceIdentifierError
from mock import MagicMock
from unittest import TestCase
from datetime import timedelta
from ebu_tt_live.clocks.local import LocalMachineClock

class TestSimpleConsumerUnit(TestCase):

    def setUp(self):
        carriage = MagicMock(spec=IConsumerCarriage)
        carriage.provides.return_value = EBUTT3Document

        self.consumer = SimpleConsumer(
            node_id='testConsumer',
            consumer_carriage=carriage
        )

    def test_process_document(self):
        # This is not quite unit... this is integration test
        doc = EBUTT3Document(
            time_base='clock',
            clock_mode='local',
            lang='en-GB',
            sequence_identifier='testSequenceEncoder01',
            sequence_number='1'
        )

        self.consumer.process_document(document=doc, availability_time=timedelta())

        self.assertIsInstance(self.consumer._sequence, EBUTT3DocumentSequence)
        self.assertIsInstance(self.consumer.reference_clock, LocalMachineClock)

    def test_process_two_documents_ignore_second_sequence_id(self):

        first_sequence =  EBUTT3Document(
            time_base='clock',
            clock_mode='local',
            lang='en-GB',
            sequence_identifier='testSequenceEncoder01',
            sequence_number='1'
        )

        second_sequence = EBUTT3Document(
            time_base='clock',
            clock_mode='local',
            lang='en-GB',
            sequence_identifier='testSequenceEncoder02',
            sequence_number='1'
        )

        self.consumer.process_document(document=first_sequence)
        self.assertIsInstance(self.consumer._sequence, EBUTT3DocumentSequence)
        self.assertIsInstance(self.consumer.reference_clock, LocalMachineClock)

        with self.assertRaises(UnexpectedSequenceIdentifierError) as context:
            self.consumer.process_document(document=second_sequence)

        self.assertTrue('Rejecting new sequence identifier' in context.exception.message)


    def test_control_request(self):
        # The message must be ignored

        message = EBUTTAuthorsGroupControlRequest(
            sequence_identifier='TestSequence',
            sender='sender',
            recipient=['one', 'two'],
            payload='Test payload'
        )

        self.consumer.process_document(document=message)

        self.assertIsNone(self.consumer._sequence)
        self.assertIsNone(self.consumer.reference_clock)
