
from unittest import TestCase
from datetime import timedelta
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.node import SimpleConsumer
from ebu_tt_live.carriage.interface import IConsumerCarriage
from mock import MagicMock


class SCDocumentProcessingTest(TestCase):

    def _get_timing_type(self, value):
        return LimitedClockTimingType(value)

    def _create_document(self, sequence_number, begin, end):
        doc = EBUTT3Document(
            time_base='clock',
            clock_mode='local',
            lang='en-gb',
            sequence_identifier='ConsumerTest',
            sequence_number=sequence_number
        )
        doc.set_begin(self._get_timing_type(timedelta(seconds=begin)))
        doc.set_end(self._get_timing_type(timedelta(seconds=end)))
        doc.availability_time = timedelta()
        return doc

    def _create_simple_consumer(self):
        carriage = MagicMock(spec=IConsumerCarriage)
        carriage.provides.return_value = EBUTT3Document
        self.consumer = SimpleConsumer(
            'consumer-testing',
            consumer_carriage=carriage
        )

    def setUp(self):
        self._create_simple_consumer()

    def test_duplicate_sequence_number_insert(self):
        doc1 = self._create_document(1, 1, 2)
        doc2 = self._create_document(2, 3, 4)
        doc3 = self._create_document(3, 4, 5)
        # Here is the duplicate
        doc4 = self._create_document(2, 2, 3)
        self.consumer.process_document(doc1)
        self.consumer.process_document(doc2)
        self.consumer.process_document(doc3)
        # This should work regardless of duplication. Ignoring this document
        self.consumer.process_document(doc4)