from .common import ConfigurableComponent, Namespace
from ebu_tt_live import clocks


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


def clock_by_type(clock_type):
    if clock_type == 'utc':
        return UTCClock
    if clock_type == 'local':
        return LocalMachineClock
    elif clock_type == 'auto':
        return DummyClock
