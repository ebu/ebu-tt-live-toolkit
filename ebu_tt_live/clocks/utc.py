from datetime import datetime, timedelta
from .base import Clock


class UTCClock(Clock):

    _time_base = 'clock'
    _clock_mode = 'utc'

    def get_real_clock_time(self):
        now = datetime.utcnow().time()
        return timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
