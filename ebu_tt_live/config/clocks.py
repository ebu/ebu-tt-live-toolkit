import logging
from .common import ConfigurableComponent, Namespace
from ebu_tt_live import clocks
from datetime import datetime, timedelta
import re
from ebu_tt_live.errors import ConfigurationError
from ebu_tt_live.strings import ERR_NO_SUCH_COMPONENT


log = logging.getLogger(__name__)


class LocalMachineClock(ConfigurableComponent):

    def __init__(self, config, local_config):
        super(LocalMachineClock, self).__init__(config, local_config)
        self.component = clocks.local.LocalMachineClock()


class UTCClock(ConfigurableComponent):

    def __init__(self, config, local_config):
        super(UTCClock, self).__init__(config, local_config)
        self.component = clocks.utc.UTCClock()


class DummyClock(ConfigurableComponent):
    """
    This wrapper returns None for reference clock allowing the consumer to create a reference clock from the first
    document received
    """
    component = None


clock_by_type = {
    'utc': UTCClock,
    'local': LocalMachineClock,
    'auto': DummyClock
}


def get_clock(clock_type):
    try:
        return clock_by_type[clock_type]
    except KeyError:
        raise ConfigurationError(
            ERR_NO_SUCH_COMPONENT.format(
                type_name=clock_type
            )
        )

def _int_or_zero(value):
    try:
        return int(value)
    except TypeError:
        return 0

_datetime_groups_regex = re.compile('([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])T([0-9][0-9]):([0-5][0-9]):([0-5][0-9]|60)(?:\.([0-9]+))?([A-Z]+)?')

def get_date(date):
    m = _datetime_groups_regex.match(date)
    years, months, days, hours, minutes, seconds, microseconds = map(
        lambda x: _int_or_zero(x),
        m.group(1, 2, 3, 4, 5, 6, 7)
    )
    
    tz = m.group(8)
    if tz is not None and tz != 'Z':
        log.warning('Ignoring provided timezone {}'.format(tz))

    return datetime(
        year = years, 
        month = months,
        day = days,
        hour = hours,
        minute = minutes,
        second = seconds,
        microsecond = microseconds
        )
