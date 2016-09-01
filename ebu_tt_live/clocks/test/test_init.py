
from unittest import TestCase
from ebu_tt_live.clocks.utc import UTCClock
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.clocks.media import MediaClock, SMPTEClock
from ebu_tt_live.clocks import get_clock


class TestInit(TestCase):

    def test_get_clock(self):
        clock = get_clock(time_base='clock', clock_mode='local')
        self.assertIsInstance(clock, LocalMachineClock)
        clock = get_clock(time_base='clock', clock_mode='utc')
        self.assertIsInstance(clock, UTCClock)
        clock = get_clock(time_base='media')
        self.assertIsInstance(clock, MediaClock)
        clock = get_clock(time_base='smpte')
        self.assertIsInstance(clock, SMPTEClock)
