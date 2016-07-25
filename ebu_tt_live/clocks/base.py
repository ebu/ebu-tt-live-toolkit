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
    _fixed_time = None
    _use_fixed_time = False

    def get_time(self):
        """
        :return: datetime.timedelta object
        """
        if self._use_fixed_time:
            return self._fixed_time
        else:
            return self.get_real_clock_time()

    def get_real_clock_time(self):
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

    def set_fixed_time(self, value):
        """
        Registers a time in the Clock object. If fixed-time mode is active, e.g. `set_fixed_time_mode(true)`
        was called on self, then every call to `get_time()` will return the registered time. The parameter
        `value` must contain the time as a datetime.timedelta. If it is not a datetime.timedelta, a `TypeError`
        exception will be raised.
        :param value: the time to register as the fixed time of the Clock. Must of type datetime.timedelta
        """
        if not isinstance(value, timedelta):
            raise TypeError
        self._fixed_time = value

    def set_fixed_time_mode(self, value):
        """
        Used to activate or deactivate the fixed-time mode. If `value` is True the clock will be set in
        fixed-time mode, while this mode is active any call to `get_time()` will return the time registered
        with `set_fixed_time` as the fixed time of clock. If `value` is False, the fixed-time mode is
        deactivated and the real time of the clock is returned when `get_time()` is called. If `value` is not of
        type `bool` a TypeError exception will be raised.
        :param value: a bool. True to activate fixed-time mode, False to deactivate fixed-time mode.
        """
        if not isinstance(value, bool):
            raise TypeError
        self._use_fixed_time = value

    def is_fixed_time_mode(self):
        """
        Returns the current status of the fixed-time mode.
        :return: True if fixed-time mode is currently active, False otherwise.
        """
        return self._use_fixed_time

    def start(self):
        pass

    def stop(self):
        pass
