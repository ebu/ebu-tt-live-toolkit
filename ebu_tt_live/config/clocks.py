from .common import ConfigurableComponent, Namespace
from ebu_tt_live import clocks


class LocalMachineClock(ConfigurableComponent):

    def __init__(self, config, local_config):
        super(LocalMachineClock, self).__init__(config, local_config)
        self.component = clocks.local.LocalMachineClock()


def clock_by_type(clock_type):
    if clock_type == 'local':
        return LocalMachineClock
