
from datetime import timedelta
from unittest import TestCase

from ebu_tt_live.clocks.utc import UTCClock


class TestUTCClock(TestCase):

    def test_instantiation(self):
        clock = UTCClock()
        self.assertIsInstance(clock.get_time(), timedelta)
