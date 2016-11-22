from .common import ConfigurableComponent, Namespace
from ebu_tt_live import clocks


class LocalMachineClock(ConfigurableComponent):

    @classmethod
    def configure(cls, config, local_config):
        return clocks.local.LocalMachineClock()


def clock_for_type(clock_type):
    if clock_type == 'local':
        return LocalMachineClock
