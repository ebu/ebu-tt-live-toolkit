from datetime import datetime, timedelta
from collections import namedtuple
from ebu_tt_live.errors import TimeFormatError
from ebu_tt_live.strings import ERR_TIME_WRONG_FORMAT
from .local import Clock


ReferenceTime = namedtuple('ReferenceTime', ['local', 'remote'])


class MediaClock(Clock):
    """
    MediaClock is a reference clock that simulates the mediastream's time by interpolating the local machine time
    from the last adjusted reference time.
    """
    _reference_mapping = None
    _time_base = 'media'

    def __init__(self):
        self.adjust_time(timedelta())

    def get_machine_time(self):
        now = datetime.now().time()
        current_time = timedelta(hours=now.hour,minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        return current_time

    def get_media_time(self, real_clock_timedelta):
        return self._reference_mapping.remote + (real_clock_timedelta - self._reference_mapping.local)

    def get_real_clock_time(self):
        return self._reference_mapping.remote + (self.get_machine_time() - self._reference_mapping.local)

    def adjust_time(self, current_time, local_time=None):
        """
        By default the current local time is used as reference point but optionally can be adjusted to a given time
        :param current_time:
        :param local_time:
        :return:
        """
        if not isinstance(current_time, timedelta) or local_time is not None and not isinstance(local_time, timedelta):
            raise TimeFormatError(ERR_TIME_WRONG_FORMAT)
        if local_time is None:
            local_time = self.get_machine_time()
        self._reference_mapping = ReferenceTime(local_time, current_time)


class SMPTEClock(MediaClock):

    _time_base = 'smpte'
    _framerate = None
    _framerate_multiplier = None
    _drop_mode = None
