
from datetime import timedelta
from unittest import TestCase

from ebu_tt_live.clocks.local import LocalMachineClock


class TestLocalClock(TestCase):

    def test_instantiation(self):
        clock = LocalMachineClock()
        self.assertIsInstance(clock.get_time(), timedelta)
