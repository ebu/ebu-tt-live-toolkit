
from unittest import TestCase
from ebu_tt_live.clocks.utc import UTCClock
from datetime import timedelta


class TestUTCClock(TestCase):

    def test_instantiation(self):
        clock = UTCClock()
        self.assertIsInstance(clock.get_time(), timedelta)
