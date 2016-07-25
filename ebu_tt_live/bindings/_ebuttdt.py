# -*- coding: utf-8 -*-
from raw._ebuttdt import *
from raw import _ebuttdt as ebuttdt_raw
from datetime import timedelta
import re
from pyxb.exceptions_ import SimpleTypeValueError
from ebu_tt_live.errors import TimeFormatOverflowError
from ebu_tt_live.strings import ERR_TIME_FORMAT_OVERFLOW


def _get_time_members(checked_time):
    hours, seconds = divmod(checked_time.seconds, 3600)
    hours += checked_time.days * 24
    minutes, seconds = divmod(seconds, 60)
    milliseconds, _ = divmod(checked_time.microseconds, 1000)
    return hours, minutes, seconds, milliseconds


class _TimedeltaBindingMixin(object):
    """
    Wiring in timedelta assignment and conversion operators
    """

    @classmethod
    def _ConvertArguments_vx(cls, args, kw):
        result = []
        for item in args:
            if isinstance(item, timedelta):
                result.append(cls.from_timedelta(item))
            else:
                result.append(item)
        return tuple(result)

    @property
    def timedelta(self):
        return self.as_timedelta(self)


class TimecountTimingType(_TimedeltaBindingMixin, ebuttdt_raw.timecountTimingType):
    """
    Extending the string type with conversions to and from timedelta
    """

    # NOTE: Update this regex should the spec change about this type
    _groups_regex = re.compile('(?P<numerator>[0-9]+(?:\\.[0-9]+)?)(?P<unit>h|ms|s|m)')

    @classmethod
    def as_timedelta(cls, instance):
        """
        Group expression with regex than switch on unit to create timedelta.
        :param instance:
        :return:
        """
        numerator, unit = cls._groups_regex.match(instance).groups()
        numerator = int(numerator)
        if unit == 's':
            return timedelta(seconds=numerator)
        elif unit == 'm':
            return timedelta(minutes=numerator)
        elif unit == 'h':
            return timedelta(hours=numerator)
        elif unit == 'ms':
            return timedelta(milliseconds=numerator)
        else:
            raise SimpleTypeValueError()

    @classmethod
    def from_timedelta(cls, instance):
        """
        Convert to one dimensional value.
        Find the smallest unit and create value using that.
        Consistency is ensured to the millisecond. Below that the number will be trimmed.
        :param instance:
        :return:
        """
        # Get the edge case out of the way even though validation will catch a 0 duration later
        if not instance:
            return '0s'
        hours, minutes, seconds, milliseconds = _get_time_members(instance)
        multiplier = 1
        numerator = 0
        unit = None
        if milliseconds:
            unit = 'ms'
            numerator += milliseconds
            multiplier *= 1000  # For the next level values so that the algo does not need to look back
        if unit or seconds:
            if not unit:
                unit = 's'
            numerator += seconds * multiplier
            multiplier *= 60
        if unit or minutes:
            if not unit:
                unit = 'm'
            numerator += minutes * multiplier
            multiplier *= 60
        if unit or hours:
            if not unit:
                unit = 'h'
            numerator += hours * multiplier
        return '{}{}'.format(numerator, unit)


ebuttdt_raw.timecountTimingType._SetSupersedingClass(TimecountTimingType)


class FullClockTimingType(_TimedeltaBindingMixin, ebuttdt_raw.fullClockTimingType):
    """
    Extending the string type with conversions to and from timedelta
    """

    _groups_regex = re.compile('([0-9][0-9]+):([0-5][0-9]):([0-5][0-9]|60)(?:\.([0-9]+))?')

    @classmethod
    def as_timedelta(cls, instance):
        """
        Using regex parse value and create timedelta
        :param instance:
        :return:
        """
        hours, minutes, seconds, milliseconds = map(lambda x: int(x), cls._groups_regex.match(instance).groups())
        return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

    @classmethod
    def from_timedelta(cls, instance):
        """
        Generate full clock type from timedelta
        :param instance:
        :return:
        """
        hours, minutes, seconds, milliseconds = _get_time_members(instance)
        if milliseconds:
            return '{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}'.format(
                hours=hours,
                minutes=minutes,
                seconds=seconds,
                milliseconds=milliseconds
            )
        else:
            return '{hours:02d}:{minutes:02d}:{seconds:02d}'.format(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            )


ebuttdt_raw.fullClockTimingType._SetSupersedingClass(FullClockTimingType)


class LimitedClockTimingType(_TimedeltaBindingMixin, ebuttdt_raw.limitedClockTimingType):
    """
    Extending the string type with conversions to and from timedelta
    """

    _groups_regex = re.compile('([0-9][0-9]):([0-5][0-9]):([0-5][0-9]|60)(?:\.([0-9]+))?')

    @classmethod
    def as_timedelta(cls, instance):
        """
        Using regex parse value and create timedelta
        :param instance:
        :return:
        """
        hours, minutes, seconds, milliseconds = map(lambda x: int(x), cls._groups_regex.match(instance).groups())
        return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

    @classmethod
    def from_timedelta(cls, instance):
        """
        Generate limited clock type from timedelta
        :param instance:
        :return:
        """
        hours, minutes, seconds, milliseconds = _get_time_members(instance)
        # We have our most significant value. Time for range check
        if hours > 99:
            raise TimeFormatOverflowError(ERR_TIME_FORMAT_OVERFLOW)
        if milliseconds:
            return '{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}'.format(
                hours=hours,
                minutes=minutes,
                seconds=seconds,
                milliseconds=milliseconds
            )
        else:
            return '{hours:02d}:{minutes:02d}:{seconds:02d}'.format(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            )


ebuttdt_raw.limitedClockTimingType._SetSupersedingClass(LimitedClockTimingType)


# Here comes the tricky one. The SMPTE requires knowledge about frames. The top level tt element knows the frameRate.
# Unfortunately the conversion methods run before the object gets created let alone inserted into a document structure.
# The conversion paradigm of storing data in the xml datatype does not work here. A deferred method is needed that
# will compute the appropriate value when the element is inserted into the document structure.
class SMPTETimingType(_TimedeltaBindingMixin, ebuttdt_raw.smpteTimingType):
    """
    Extending the string type with conversions to and from timedelta
    """
    @classmethod
    def as_timedelta(cls, instance):
        pass

    @classmethod
    def from_timedelta(cls, instance):
        pass


# TODO: SMPTE frameRate and frameRateMultiplier value from tt element.
# ebuttdt_raw.smpteTimingType._SetSupersedingClass(SMPTETimingType)
