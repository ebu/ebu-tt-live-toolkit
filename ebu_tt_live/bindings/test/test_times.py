
from unittest import TestCase
from unittest import skip, SkipTest
from datetime import timedelta
from ebu_tt_live.bindings import ebuttdt
from pyxb import SimpleTypeValueError, SimpleFacetValueError

class TestTimecountTimingType(TestCase):

    _test_cases = {
        '1.3s': timedelta(seconds = 1, milliseconds = 300),
        '1.03s': timedelta(seconds = 1, milliseconds = 30),
        '1.30s': timedelta(seconds = 1, milliseconds = 300),
        '1s': timedelta(seconds = 1),
        '1.3m': timedelta(minutes = 1, seconds = 18),
        '1.03m': timedelta(minutes = 1, seconds = 1, milliseconds = 800),
        '1.30m': timedelta(minutes = 1, seconds = 18),
        '1m': timedelta(minutes = 1),
        '1.3h': timedelta(hours = 1, minutes = 18),
        '1.03h': timedelta(hours = 1, minutes = 1, seconds = 48),
        '1.30h': timedelta(hours = 1, minutes = 18),
        '1h': timedelta(hours = 1),
        '1.3ms': timedelta(milliseconds = 1, microseconds = 300),
        '1.03ms': timedelta(milliseconds = 1, microseconds = 30),
        '1.30ms': timedelta(milliseconds = 1, microseconds = 300),
        '1ms': timedelta(milliseconds = 1),
    }

    _type_class = ebuttdt.TimecountTimingType

    def test_as_timedelta(self):
        for t, td in self._test_cases.items() :
            test_instance = self._type_class(t)
            self.assertEqual(test_instance.timedelta, td)
            assert test_instance == t



class TestFullClockTimingType(TestCase):

    _test_cases = {
        '111:22:33': timedelta(hours = 111, minutes = 22, seconds = 33),
        '111:22:33.4': timedelta(hours = 111, minutes = 22, seconds = 33, milliseconds = 400),
        '111:22:33.04': timedelta(hours = 111, minutes = 22, seconds = 33, milliseconds = 40),
        '111:22:33.40': timedelta(hours = 111, minutes = 22, seconds = 33, milliseconds = 400),
    }

    _type_class = ebuttdt.FullClockTimingType

    def test_as_timedelta(self):
        for t, td in self._test_cases.items() :
            test_instance = self._type_class(t)
            self.assertEqual(test_instance.timedelta, td)
            assert test_instance == t


class TestLimitedClockTimingType(TestCase):

    _test_cases = {
        '11:22:33': timedelta(hours = 11, minutes = 22, seconds = 33),
        '11:22:33.4': timedelta(hours = 11, minutes = 22, seconds = 33, milliseconds = 400),
        '11:22:33.04': timedelta(hours = 11, minutes = 22, seconds = 33, milliseconds = 40),
        '11:22:33.40': timedelta(hours = 11, minutes = 22, seconds = 33, milliseconds = 400),
    }
    
    _type_class = ebuttdt.LimitedClockTimingType

    def test_as_timedelta(self):
        for t, td in self._test_cases.items() :
            test_instance = self._type_class(t)
            self.assertEqual(test_instance.timedelta, td)
            assert test_instance == t
