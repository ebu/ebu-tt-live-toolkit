from .common import ConfigurableComponent, Namespace
from ebu_tt_live import clocks
from ebu_tt_live.errors import ConfigurationError
from ebu_tt_live.strings import ERR_NO_SUCH_COMPONENT


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
