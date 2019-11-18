
from unittest import TestCase
from datetime import timedelta
from ebu_tt_live.bindings.converters.timedelta_converter import \
    FixedOffsetSMPTEtoTimedeltaConverter
from ebu_tt_live.errors import TimeFormatError, TimeNegativeError
from ebu_tt_live.strings import ERR_TIME_FRAMES_OUT_OF_RANGE, \
    ERR_TIME_FRAME_IS_DROPPED, ERR_TIME_NEGATIVE


class TestFixedOffsetSMPTEtoTimedeltaConverter(TestCase):
    
    def test_effective_framerate_rational(self):
        efr = \
            FixedOffsetSMPTEtoTimedeltaConverter.\
            _calc_effective_frame_rate(frameRate=30,
                                       frameRateMultiplier='998 1000')

        self.assertEqual(efr, 29.94)
        assert efr == 29.94

    def test_effective_framerate_irrational(self):
        efr = \
            FixedOffsetSMPTEtoTimedeltaConverter.\
            _calc_effective_frame_rate(frameRate=30,
                                       frameRateMultiplier='1000 1001')

        self.assertAlmostEqual(efr, 29.97002997)

    def test_dropped_frames_nondrop(self):
        conv = \
            FixedOffsetSMPTEtoTimedeltaConverter('10:00:00:00',
                                                 '30',
                                                 '1000 1001',
                                                 'nonDrop')
        df = conv._dropped_frames(1, 1)
        self.assertEqual(df, 0)

    def test_dropped_frames_ntsc(self):
        conv = \
            FixedOffsetSMPTEtoTimedeltaConverter('10:00:00:00',
                                                 '30',
                                                 '1000 1001',
                                                 'dropNTSC')
        df = conv._dropped_frames(1, 1)
        self.assertEqual(df, 110)

    def test_dropped_frames_pal(self):
        conv = \
            FixedOffsetSMPTEtoTimedeltaConverter('10:00:00:00',
                                                 '30',
                                                 '1000 1001',
                                                 'dropPAL')
        df = conv._dropped_frames(1, 1)
        self.assertEqual(df, 108)

    def test_counted_frames(self):
        conv = \
            FixedOffsetSMPTEtoTimedeltaConverter('10:00:00:00',
                                                 '30',
                                                 '1000 1001',
                                                 'nonDrop')
        self.assertEqual(conv._counted_frames(3, 57, 12, 17), 426977)

    def test_convert_timecode_25_1_1(self):
        conv = \
            FixedOffsetSMPTEtoTimedeltaConverter('10:00:00:00',
                                                 '25',
                                                 '1 1',
                                                 'nonDrop')
        self.assertEqual(conv.timedelta('10:00:00:00'), timedelta(seconds=0))
        self.assertEqual(conv.timedelta('11:12:13:14'), 
                         timedelta(seconds=4333.56))

    def test_convert_timecode_30_1000_1001(self):
        conv = \
            FixedOffsetSMPTEtoTimedeltaConverter('10:00:00:00',
                                                 '30',
                                                 '1000 1001',
                                                 'dropNTSC')
        self.assertEqual(conv.timedelta('10:00:00:00'), timedelta(seconds=0))
        self.assertAlmostEqual(conv.timedelta('11:12:13:14').total_seconds(), 
                               4333.4625, 4)

    def test_can_convert(self):
        conv = \
            FixedOffsetSMPTEtoTimedeltaConverter('10:00:00:00',
                                                 '25',
                                                 '1 1',
                                                 'nonDrop')
        self.assertTrue(conv.can_convert('10:00:00:24'))
        self.assertFalse(conv.can_convert('09:59:59:24'))

    def test_raise_exception_if_too_many_frames(self):
        conv = \
            FixedOffsetSMPTEtoTimedeltaConverter('10:00:00:00',
                                                 '25',
                                                 '1 1',
                                                 'nonDrop')
        with self.assertRaises(TimeFormatError,
                               msg=ERR_TIME_FRAMES_OUT_OF_RANGE):
            conv.can_convert('10:00:00:25')

    def test_raise_exception_if_dropped_frame_NTSC(self):
        conv = \
            FixedOffsetSMPTEtoTimedeltaConverter('10:00:00:00',
                                                 '30',
                                                 '1000 1001',
                                                 'dropNTSC')
        with self.assertRaises(TimeFormatError,
                               msg=ERR_TIME_FRAME_IS_DROPPED):
            conv.can_convert('10:01:00:00')
        with self.assertRaises(TimeFormatError,
                               msg=ERR_TIME_FRAME_IS_DROPPED):
            conv.can_convert('10:01:00:01')

        # Check a not dropped frame value works fine too
        conv.can_convert('10:01:00:02')

        pass

    def test_raise_exception_if_dropped_frame_PAL(self):
        conv = \
            FixedOffsetSMPTEtoTimedeltaConverter('10:00:00:00',
                                                 '30',
                                                 '1000 1001',
                                                 'dropPAL')
        with self.assertRaises(TimeFormatError,
                               msg=ERR_TIME_FRAME_IS_DROPPED):
            conv.can_convert('10:02:00:00')
        with self.assertRaises(TimeFormatError,
                               msg=ERR_TIME_FRAME_IS_DROPPED):
            conv.can_convert('10:02:00:02')
        with self.assertRaises(TimeFormatError,
                               msg=ERR_TIME_FRAME_IS_DROPPED):
            conv.can_convert('10:02:00:03')

        # Check a not dropped frame value works fine too
        conv.can_convert('10:02:00:04')

        pass

    def test_raise_exception_if_negative(self):
        conv = \
            FixedOffsetSMPTEtoTimedeltaConverter('10:00:00:00',
                                                 '25',
                                                 '1 1',
                                                 'nonDrop')

        # Should convert without raising an exception
        self.assertEqual(conv.timedelta('10:00:00:24'),
                         timedelta(milliseconds=960))
        with self.assertRaises(TimeNegativeError,
                               msg=ERR_TIME_NEGATIVE):
            conv.timedelta('09:59:59:24')
        pass
