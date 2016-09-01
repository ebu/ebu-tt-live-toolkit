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

        self.document1 = self._create_document(1, 2)
        self.document2 = self._create_document(3, 4)
        self.document3 = self._create_document(5, 6)

    def test_sequence_add1(self):
        """
        This tests an out of order document reception
        :return:
        """
        self.sequence.add_document(self.document1)
        self.sequence.add_document(self.document3)
        self.sequence.add_document(self.document2)

        self.assertEqual(
            self.document1.resolved_begin_time,
            timedelta(seconds=1)
        )
        self.assertEqual(
            self.document2.resolved_begin_time,
            timedelta(seconds=3)
        )
        self.assertEqual(
            self.document3.resolved_begin_time,
            timedelta(seconds=5)
        )

        self.assertEqual(
            self.document1.resolved_end_time,
            timedelta(seconds=2)
        )
        self.assertEqual(
            self.document2.resolved_end_time,
            timedelta(seconds=4)
        )
        self.assertEqual(
            self.document3.resolved_end_time,
            timedelta(seconds=6)
        )

    def test_sequence_add2(self):
        """
        This test swaps 2 sequence numbers thereby creating an erasure
        :return:
        """
        self.document2.sequence_number = 3
        self.document3.sequence_number = 2
        self.document2.validate()
        self.document3.validate()
        self.document1.validate()

        self.sequence.add_document(self.document1)
        self.sequence.add_document(self.document3)
        self.sequence.add_document(self.document2)

        # We expect document2 to erase document3
        # TODO: Finish these on this unittesting level

    # SPEC-CONFORMANCE : R9
    def test_increasing_sequence_number(self):
        self.assertGreater(self.document2.sequence_number, self.document1.sequence_number)
        self.assertGreater(self.document3.sequence_number, self.document2.sequence_number)
