
from unittest import TestCase
from ebu_tt_live.clocks.base import Clock
from datetime import timedelta


class TestLocalClock(TestCase):

    def test_fixed_time_case(self):
        clock = Clock()
        test_time = timedelta(hours=1)
        clock.set_fixed_time(test_time)
        clock.set_fixed_time_mode(True)
        self.assertEqual(clock.get_time(), test_time)
        clock.set_fixed_time_mode(False)
        self.assertRaises(NotImplementedError, lambda: clock.get_time())
        self.assertRaises(TypeError, lambda: clock.set_fixed_time(1))
