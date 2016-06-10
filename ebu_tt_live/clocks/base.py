
class Clock(object):
    """
    This class represents our timing source that we use to get time related
    information when document processing happens. Most of the utility
    functions are meant to stay here and the subclasses should implement get_time only.
    """

    _clock_mode = None
    _time_base = None

    def get_time(self):
        """
        Implemented in descendant classes
        :return: datetime.timedelta object
        """
        raise NotImplementedError()

    @property
    def clock_mode(self):
        return self._clock_mode

    @clock_mode.setter
    def clock_mode(self, value):
        self._clock_mode = value

    @property
    def time_base(self):
        return self._time_base

    def start(self):
        pass

    def stop(self):
        pass
