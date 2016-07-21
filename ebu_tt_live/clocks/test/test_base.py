
from unittest import TestCase
from ebu_tt_live.clocks.local import Clock
from datetime import timedelta, datetime
import pytest


class TestBaseClock(TestCase):

    def test_saved_time(self):
        clock = Clock()
        test_time = datetime.now().time()
        test_time_timedelta = timedelta(hours=test_time.hour, minutes=test_time.minute, seconds=test_time.second, microseconds=test_time.microsecond)
        clock.saved_time = test_time_timedelta
        self.assertEqual(clock.saved_time, test_time_timedelta)
        with pytest.raises(TypeError):
            clock.saved_time = 3
