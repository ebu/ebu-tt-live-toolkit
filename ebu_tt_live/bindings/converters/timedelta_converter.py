from datetime import timedelta
import re
from math import floor
from ebu_tt_live.strings import ERR_TIME_NEGATIVE, \
    ERR_TIME_FRAMES_OUT_OF_RANGE, \
    ERR_TIME_FRAME_IS_DROPPED
from ebu_tt_live.errors import TimeNegativeError, TimeFormatError


class ISMPTEtoTimedeltaConverter(object):

    def __init__(self):
        raise NotImplementedError()

    def timedelta(smpte_time):
        raise NotImplementedError()

    def can_convert(smpte_time):
        raise NotImplementedError()


class FixedOffsetSMPTEtoTimedeltaConverter(ISMPTEtoTimedeltaConverter):
    """
    Converts SMPTE timecodes to timedeltas with a fixed offset.

    This converter utility class uses a strategy that assumes a fixed offset,
    a reference SMPTE timecode value that is considered the zero point, and
    a continuous set of SMPTE timecodes monotonically increasing (aside
    from drop frames). It should not be used in cases where there may be
    discontinuities in the timecode, since it will give incorrect results.

    The object
    uses the ``frameRate``, ``frameRateMultiplier`` and ``dropMode`` to
    calculate the equivalent timedelta output value for any
    given input SMPTE timecode, and raises an exception if an attempt
    is made to convert a timecode that is earlier than the zero point.
    This can be avoided by calling :py:func:`can_convert()` to check first.

    Alternatively call :py:func:`timedelta()` directly in a ``try`` block
    and catch the :py:class:`ebu_tt_live.errors.TimeNegativeError` instead,
    which avoids essentially running the same code twice.
    """

    _smpteReferenceS = None
    _frameRate = None
    _effectiveFrameRate = None
    _dropMode = None

    _frm_regex = re.compile('(?P<numerator>\\d+)\\s(?P<denominator>\\d+)')
    _tc_regex = \
        re.compile('([0-9][0-9]):([0-5][0-9]):([0-5][0-9]):([0-9][0-9])')

    def __init__(self, smpteReference, frameRate,
                 frameRateMultiplier, dropMode):
        self._frameRate = int(frameRate)
        self._effectiveFrameRate = \
            self._calc_effective_frame_rate(
                int(frameRate), frameRateMultiplier)
        self._dropMode = dropMode
        self._smpteReferenceS = self._calculate_s(smpteReference)

    def timedelta(self, smpte_time):
        """
        Convert a timecode to a timedelta.

        :param smpte_time: The timecode value to convert
        :return timedelta: The equivalent timedelta
        :raises TimeNegativeError: if the timecode occurs before the reference zero point
        :raises TimeFormatError: if the frames value is illegal
        """
        s = self._calculate_s(smpte_time)

        if self._smpteReferenceS > s:
            raise TimeNegativeError(ERR_TIME_NEGATIVE)

        return timedelta(seconds=s-self._smpteReferenceS)

    def can_convert(self, smpte_time):
        """
        Check if a given timecode can successfully be converted to a timedelta.

        :param smpte_time: The test value
        :return Boolean: True if the timecode can successfully be converted
        :raises TimeFormatError: if the frames value is illegal
        """
        s = self._calculate_s(smpte_time)

        return self._smpteReferenceS <= s

    @classmethod
    def _calc_effective_frame_rate(cls, frameRate, frameRateMultiplier):
        # See https://www.w3.org/TR/ttml1/#time-expression-semantics-smpte
        # for the semantics of effective frame rate calculation
        frm_numerator_s, frm_denominator_s = \
            cls._frm_regex.match(frameRateMultiplier).groups()

        return float(frameRate) * \
            float(frm_numerator_s) / \
            float(frm_denominator_s)

    def _dropped_frames(self, hours, minutes):
        # See https://www.w3.org/TR/ttml1/#time-expression-semantics-smpte
        # for the semantics of dropped frame calculation
        dropped_frames = 0

        if self._dropMode == 'dropNTSC':
            dropped_frames = \
                (hours * 54 + minutes - floor(minutes/10)) * 2
        elif self._dropMode == 'dropPAL':
            dropped_frames = \
                (hours * 27 + floor(minutes / 2) - floor(minutes / 20)) * 4

        return dropped_frames

    def _counted_frames(self, hours, minutes, seconds, frames):
        # See https://www.w3.org/TR/ttml1/#time-expression-semantics-smpte
        # for the semantics of counted frame calculation
        return (3600 * hours + 60 * minutes + seconds) * \
            self._frameRate + frames

    def _calculate_s(self, smpte_time):
        # Thie method mplements
        # https://www.w3.org/TR/ttml1/#time-expression-semantics-smpte
        # which specifies the calculation of S
        hours, minutes, seconds, frames = \
            [int(x) for x in self._tc_regex.match(smpte_time).groups()]

        if frames >= self._frameRate:
            raise TimeFormatError(ERR_TIME_FRAMES_OUT_OF_RANGE)

        if self._is_dropped_frame(minutes, seconds, frames):
            raise TimeFormatError(ERR_TIME_FRAME_IS_DROPPED)

        s = (self._counted_frames(hours, minutes, seconds, frames) -
             self._dropped_frames(hours, minutes)) / \
            self._effectiveFrameRate

        return s

    def _is_dropped_frame(self, minutes, seconds, frames):
        # This method implements
        # https://www.w3.org/TR/ttml1/#parameter-attribute-dropMode 
        # which defines the rules for dropped frames.
        is_dropped_frame = False

        if seconds == 0:  # in NTSC and PAL frames are only dropped at 0s
            if self._dropMode == 'dropNTSC' and \
                    minutes not in [0, 10, 20, 30, 40, 50]:
                is_dropped_frame = frames in [0, 1]
            elif self._dropMode == 'dropPAL' and \
                    minutes % 2 == 0 and minutes not in [0, 20, 40]:
                is_dropped_frame = frames in [0, 1, 2, 3]

        return is_dropped_frame
