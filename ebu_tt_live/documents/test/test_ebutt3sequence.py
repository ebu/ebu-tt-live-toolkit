from unittest import TestCase
from datetime import timedelta, datetime
from ebu_tt_live.documents import EBUTT3Document, EBUTT3DocumentSequence
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType


class TestEBUTT3Sequence(TestCase):

    def _get_timing_type(self, value):
        if self.reference_clock.time_base == 'clock':
            return LimitedClockTimingType(value)

    def _create_document(self, begin, end):
        doc = self.sequence.new_document()
        doc.set_begin(self._get_timing_type(timedelta(seconds=begin)))
        doc.set_end(self._get_timing_type(timedelta(seconds=end)))
        doc.availability_time = timedelta()
        return doc

    def setUp(self):
        self.reference_clock = LocalMachineClock()
        self.sequence = EBUTT3DocumentSequence(
            sequence_identifier='sequenceTesting',
            reference_clock=self.reference_clock,
            lang='en-GB'
        )

        self.document1 = self._create_document(1,2)
        self.document2 = self._create_document(5, 6)
        self.document3 = self._create_document(3, 4)

    def test_sequence_add1(self):

        self.sequence.add_document(self.document1)
        self.sequence.add_document(self.document2)
        self.sequence.add_document(self.document3)
        pass
