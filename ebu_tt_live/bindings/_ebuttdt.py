# -*- coding: utf-8 -*-
from raw._ebuttdt import *
from raw import _ebuttdt as ebuttdt_raw
from datetime import timedelta
from decimal import Decimal
import re, logging
from pyxb.exceptions_ import SimpleTypeValueError, SimpleFacetValueError
from ebu_tt_live.errors import TimeFormatOverflowError, ExtentMissingError
from ebu_tt_live.strings import ERR_TIME_FORMAT_OVERFLOW, ERR_SEMANTIC_VALIDATION_TIMING_TYPE
from .pyxb_utils import get_xml_parsing_context
from .validation.base import SemanticValidationMixin
from .validation.presentation import SizingValidationMixin

log = logging.getLogger(__name__)


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

    # For each timing attribute a list of timeBases is specified, which represents the valid timeBase, timing attribute
    # and timing type semantic constraint.
    _compatible_timebases = {
        'begin': [],
        'dur': [],
        'end': []
    }

    @classmethod
    def _int_or_none(cls, value):
        try:
            return int(value)
        except TypeError:
            return 0

    @classmethod
    def compatible_timebases(cls):
        return cls._compatible_timebases

    @classmethod
    def _ConvertArguments_vx(cls, args, kw):
        """
        This hook is called before the type in question is instantiated. This is meant to do some normalization
        of input parameters and convert them to tuple. In this function we check the timeBase and the attribute name
        against our compatible_timebases mapping inside the timing type class. If an invalid scenario is encountered
        SimpleTypeValueError is raised, which effectively prevents the timingType union to instantiate the type.

        :raises pyxb.SimpleTypeValueError:
        :param args:
        :param kw:
        :return: tuple of converted input parameters.
        """
        result = []
        # In parsing mode check timebase compatibility at instantiation time. This prevents pyxb instantiating
        # the wrong type given 2 types having overlapping values in a union as it happens in full and limited
        # clock timing types.
        context = get_xml_parsing_context()
        if context is not None:
            # This means we are in XML parsing context. There should be a timeBase and a timing_attribute_name in the
            # context object.
            time_base = context['timeBase']
            timing_att_name = context['timing_attribute_name']
            if time_base not in cls._compatible_timebases[timing_att_name]:
                log.debug(ERR_SEMANTIC_VALIDATION_TIMING_TYPE.format(
                    attr_name=timing_att_name,
                    attr_type=cls,
                    attr_value=args,
                    time_base=time_base
                ))
                raise pyxb.SimpleTypeValueError(ERR_SEMANTIC_VALIDATION_TIMING_TYPE.format(
                    attr_name=timing_att_name,
                    attr_type=cls,
                    attr_value=args,
                    time_base=time_base
                ))
        for item in args:
            if isinstance(item, timedelta):
                result.append(cls.from_timedelta(item))
            else:
                result.append(item)
        return tuple(result)

    @property
    def timedelta(self):
        return self.as_timedelta(self)


class TwoDimSizingMixin(object):

    _groups_regex = None
    _1dim_format = None
    _2dim_format = None

    @classmethod
    def as_tuple(cls, instance):
        first, second = cls._groups_regex.match(instance).groups()
        return float(first), second is not None and float(second) or None

    @classmethod
    def from_tuple(cls, instance):
        if len(instance) > 1:
            if cls._2dim_format is None:
                raise SimpleTypeValueError(cls, 'This type accepts 1 dimensional values only')
            return cls._2dim_format.format(*instance)
        else:
            if cls._1dim_format is None:
                raise SimpleTypeValueError(cls, 'This type accepts 2 dimensnional values only')
            return cls._1dim_format.format(*instance)

    @property
    def horizontal(self):
        # TODO: Caching of tuple
        tup_value = self.as_tuple(self)
        if tup_value[1] is not None:
            return tup_value[0]
        else:
            return None

    @property
    def vertical(self):
        tup_value = self.as_tuple(self)
        if tup_value[1] is not None:
            return tup_value[1]
        else:
            return tup_value[0]

    @classmethod
    def _ConvertArguments_vx(cls, args, kw):
        result = []
        current_pair = []
        for item in args:
            if isinstance(item, int) or isinstance(item, float):
                current_pair.append(item)
                if len(current_pair) > 1:
                    result.append(cls.from_tuple(tuple(current_pair)))
                    current_pair = []
            else:
                result.append(item)
        if len(current_pair) > 0:
            result.append(cls.from_tuple(tuple(current_pair)))
        return tuple(result)


class TimecountTimingType(_TimedeltaBindingMixin, ebuttdt_raw.timecountTimingType):
    """
    Extending the string type with conversions to and from timedelta
    """

    # NOTE: Update this regex should the spec change about this type
    _groups_regex = re.compile('(?P<numerator>[0-9]+(?:\\.[0-9]+)?)(?P<unit>h|ms|s|m)')
    # TODO: Consult and restrict this in an intuitive way to avoid awkward timing type combinations on the timing attributes.
    _compatible_timebases = {
        'begin': ['clock', 'media'],
        'dur': ['clock', 'media'],
        'end': ['clock', 'media']
    }

    @classmethod
    def as_timedelta(cls, instance):
        """
        Group expression with regex than switch on unit to create timedelta.
        :param instance:
        :return:
        """
        numerator, unit = cls._groups_regex.match(instance).groups()
        numerator = float(numerator)
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


class FullClockTimingType(SemanticValidationMixin, _TimedeltaBindingMixin, ebuttdt_raw.fullClockTimingType):
    """
    Extending the string type with conversions to and from timedelta
    """

    _compatible_timebases = {
        'begin': ['media'],
        'dur': ['media'],
        'end': ['media']
    }
    _groups_regex = re.compile('([0-9][0-9]+):([0-5][0-9]):([0-5][0-9]|60)(?:\.([0-9]+))?')

    @classmethod
    def compatible_timebases(cls):
        return cls._compatible_timebases

    @classmethod
    def as_timedelta(cls, instance):
        """
        Using regex parse value and create timedelta
        :param instance:
        :return:
        """
        hours, minutes, seconds, milliseconds = map(
            lambda x: cls._int_or_none(x),
            cls._groups_regex.match(instance).groups()
        )
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

    _compatible_timebases = {
        'begin': ['clock'],
        'dur': ['clock'],
        'end': ['clock']
    }
    _groups_regex = re.compile('([0-9][0-9]):([0-5][0-9]):([0-5][0-9]|60)(?:\.([0-9]+))?')

    @classmethod
    def as_timedelta(cls, instance):
        """
        Using regex parse value and create timedelta
        :param instance:
        :return:
        """
        hours, minutes, seconds, milliseconds = map(
            lambda x: cls._int_or_none(x),
            cls._groups_regex.match(instance).groups()
        )
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
    _compatible_timebases = {
        'begin': ['smpte'],
        'dur': ['smpte'],
        'end': ['smpte']
    }

    @classmethod
    def as_timedelta(cls, instance):
        # TODO: implement SMPTE
        return timedelta()

    @classmethod
    def from_timedelta(cls, instance):
        # TODO: implement SMPTE
        return SMPTETimingType('00:00:00:00')


# TODO: SMPTE frameRate and frameRateMultiplier value from tt element.
ebuttdt_raw.smpteTimingType._SetSupersedingClass(SMPTETimingType)


class PixelOriginType(TwoDimSizingMixin, SizingValidationMixin, ebuttdt_raw.pixelOriginType):

    _groups_regex = re.compile('(?:[+-]?(?P<first>\d*\.?\d+)(?:px))\s(?:[+-]?(?P<second>\d*\.?\d+)(?:px))')
    _2dim_format = '{}px {}px'

    def _semantic_validate_sizing_context(self, dataset):
        extent = dataset['tt_element'].extent
        if extent is None:
            raise ExtentMissingError(self)

ebuttdt_raw.pixelOriginType._SetSupersedingClass(PixelOriginType)


class CellOriginType(TwoDimSizingMixin, ebuttdt_raw.cellOriginType):

    _groups_regex = re.compile('(?:[+-]?(?P<first>\d*\.?\d+)(?:c))\s(?:[+-]?(?P<second>\d*\.?\d+)(?:c))')
    _2dim_format = '{}c {}c'

ebuttdt_raw.cellOriginType._SetSupersedingClass(CellOriginType)


class PercentageOriginType(TwoDimSizingMixin, ebuttdt_raw.percentageOriginType):

    _groups_regex = re.compile('(?:[+-]?(?P<first>\d*\.?\d+)(?:%))\s(?:[+-]?(?P<second>\d*\.?\d+)(?:%))')
    _2dim_format = '{}% {}%'

ebuttdt_raw.percentageOriginType._SetSupersedingClass(PercentageOriginType)


class PixelExtentType(SizingValidationMixin, ebuttdt_raw.pixelExtentType):

    def _semantic_validate_sizing_context(self, dataset):
        extent = dataset['tt_element'].extent
        if extent is None:
            raise ExtentMissingError(self)


ebuttdt_raw.pixelExtentType._SetSupersedingClass(PixelExtentType)


class PixelLengthType(SizingValidationMixin, ebuttdt_raw.pixelLengthType):

    def _semantic_validate_sizing_context(self, dataset):
        extent = dataset['tt_element'].extent
        if extent is None:
            raise ExtentMissingError(self)


ebuttdt_raw.pixelLengthType._SetSupersedingClass(PixelLengthType)


class PercentageLengthType(ebuttdt_raw.percentageLengthType):
    pass


ebuttdt_raw.percentageLengthType._SetSupersedingClass(PercentageLengthType)


class CellLengthType(ebuttdt_raw.cellLengthType):
    pass


ebuttdt_raw.cellLengthType._SetSupersedingClass(CellLengthType)


class PixelFontSizeType(TwoDimSizingMixin, SizingValidationMixin, ebuttdt_raw.pixelFontSizeType):

    _groups_regex = re.compile('(?:[+]?(?P<first>\d*\.?\d+)(?:px))(?:\s(?:[+]?(?P<second>\d*\.?\d+)(?:px)))?')

    _1dim_format = '{}px'
    _2dim_format = '{}px {}px'

    def _semantic_validate_sizing_context(self, dataset):
        extent = dataset['tt_element'].extent
        if extent is None:
            raise ExtentMissingError(self)

ebuttdt_raw.pixelFontSizeType._SetSupersedingClass(PixelFontSizeType)


class CellFontSizeType(TwoDimSizingMixin, ebuttdt_raw.cellFontSizeType):

    _groups_regex = re.compile('(?:[+]?(?P<first>\d*\.?\d+)(?:c))(?:\s(?:[+]?(?P<second>\d*\.?\d+)(?:c)))?')

    _1dim_format = '{}c'
    _2dim_format = '{}c {}c'

ebuttdt_raw.cellFontSizeType._SetSupersedingClass(CellFontSizeType)


class PercentageFontSizeType(TwoDimSizingMixin, ebuttdt_raw.percentageFontSizeType):

    _groups_regex = re.compile('(?:[+]?(?P<first>\d*\.?\d+)(?:%))(?:\s(?:[+]?(?P<second>\d*\.?\d+)(?:%)))?')

    _1dim_format = '{}%'
    _2dim_format = '{}% {}%'

    def do_mul(self, other):
        if isinstance(other, CellFontSizeType):
            if other.horizontal is not None:
                return CellFontSizeType(other.vertical, other.horizontal)
            else:
                return CellFontSizeType(other.vertical)
        if isinstance(other, PixelFontSizeType):
            if other.horizontal is not None:
                return PixelFontSizeType(other.vertical, other.horizontal)
            else:
                return PixelFontSizeType(other.vertical)
        else:
            return NotImplemented

    def __mul__(self, other):
        return self.do_mul(other)

    def __rmul__(self, other):
        return self.do_mul(other)


ebuttdt_raw.percentageFontSizeType._SetSupersedingClass(PercentageFontSizeType)



