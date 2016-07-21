from datetime import timedelta


class Clock(object):
    """
    This class represents our timing source that we use to get time related
    information when document processing happens. Most of the utility
    functions are meant to stay here and the subclasses should implement get_time only.
    """

    _clock_mode = None
    _time_base = None
    # Implemented to be used with the manifest file, allows us to save a fix
    # time that we can read back later.
    _saved_time = None

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

    @property
    def saved_time(self):
        return self._saved_time

    @saved_time.setter
    def saved_time(self, value):
        if not isinstance(value, timedelta):
            raise TypeError
        else:
            self._saved_time = value

    def start(self):
        pass

    def stop(self):
        pass
