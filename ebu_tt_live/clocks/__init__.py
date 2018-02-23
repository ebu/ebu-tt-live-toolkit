
from . import base
from . import local
from . import utc
from . import media

# NOTE: Some of the code below includes handling of SMPTE time base, which was removed from version 1.0 of the specification.


def get_clock(time_base, **kwargs):
    if time_base == 'clock':
        if kwargs['clock_mode'] == 'local':
            return local.LocalMachineClock()
        elif kwargs['clock_mode'] == 'utc':
            return utc.UTCClock()
    elif time_base == 'media':
        # TODO: Here we need the reference clock identifier
        return media.MediaClock()
    elif time_base == 'smpte':
        return media.SMPTEClock()
    else:
        return None


def get_clock_from_document(document):
    # TODO: Finish with reference clock identifier
    return get_clock(
        time_base=document.time_base,
        clock_mode=document.clock_mode
    )
