
from . import base
from . import local
from . import media


def get_clock(time_base, **kwargs):
    if time_base == 'clock':
        if kwargs['clock_mode'] == 'local':
            return local.LocalMachineClock()
    elif time_base == 'media':
        # TODO: Here we need the reference clock identifier
        return media.MediaClock()
    elif time_base == 'smpte':
        return media.SMPTEClock()
