
from unittest import TestCase
from ebu_tt_live.clocks.local import LocalMachineClock
from datetime import timedelta


class TestLocalClock(TestCase):

    def test_instantiation(self):
        clock = LocalMachineClock()
        self.assertIsInstance(clock.get_time(), timedelta)
