
from ebu_tt_live.documents import EBUTT3Document, EBUTTAuthorsGroupControlRequest, EBUTT3DocumentSequence
from ebu_tt_live.node import SimpleConsumer
from ebu_tt_live.carriage import IConsumerCarriage
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

