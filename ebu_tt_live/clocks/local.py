import time


class LocalTimeClock(object):

    def get_current_time(self):
        return time.localtime()
