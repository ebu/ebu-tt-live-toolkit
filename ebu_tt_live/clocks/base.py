from datetime import timedelta
from ebu_tt_live.errors import TimeFormatError, TimeFormatOverflowError
from ebu_tt_live.strings import ERR_TIME_WRONG_FORMAT, ERR_TIME_FORMAT_OVERFLOW


class Clock(object):
    """
    This class represents our timing source that we use to get time related
    information when document processing happens. Most of the utility
    functions are meant to stay here and the subclasses should implement get_time only.
    """

    def get_time(self):
        """
        Implemented in descendant classes
        :return: datetime.timedelta object
        """
        raise NotImplementedError()

    def _check_time(self, given_time):
        if given_time is not None and not isinstance(given_time, timedelta):
            raise TimeFormatError(ERR_TIME_WRONG_FORMAT)
        if given_time is None:
            given_time = self.get_time()
        return given_time

    def _get_time_members(self, checked_time):
        hours, seconds = divmod(checked_time.seconds, 3600)
        hours += checked_time.days * 24
        minutes, seconds = divmod(seconds, 60)
        return hours, minutes, seconds, checked_time.microseconds

    def get_smpte_time(self, given_time=None):
        """
        SMPTE timeformat: ([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]:[0-9][0-9]
        :param given_time:
        :return:
        """
        checked_time = self._check_time(given_time)
        hours, minutes, seconds, microseconds = self._get_time_members(checked_time)
        # We have our most significant value. Time for range check
        if hours > 23:
            raise TimeFormatOverflowError(ERR_TIME_FORMAT_OVERFLOW)
        centiseconds, _ = divmod(microseconds, 10000)
        return '{hours:02d}:{minutes:02d}:{seconds:02d}:{centiseconds:02d}'.format(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            centiseconds=centiseconds
        )

    def get_full_clock_time(self, given_time=None):
        """
        Full timeformat: [0-9][0-9]+:[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?
        :param given_time:
        :return:
        """
        checked_time = self._check_time(given_time)
        hours, minutes, seconds, microseconds = self._get_time_members(checked_time)
        return '{hours:02d}:{minutes:02d}:{seconds:02d}.{microseconds:d}'.format(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=microseconds
        )

    def get_limited_clock_time(self, given_time=None):
        """
        Limited timeformat: [0-9][0-9]:[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?
        The number of hours is limited to 2 digits
        :param given_time:
        :return:
        """
        checked_time = self._check_time(given_time)
        hours, minutes, seconds, microseconds = self._get_time_members(checked_time)
        # We have our most significant value. Time for range check
        if hours > 99:
            raise TimeFormatOverflowError(ERR_TIME_FORMAT_OVERFLOW)
        return '{hours:02d}:{minutes:02d}:{seconds:02d}.{microseconds:d}'.format(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=microseconds
        )

    def start(self):
        pass

    def stop(self):
        pass
