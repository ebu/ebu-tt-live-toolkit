import logging
from argparse import ArgumentParser
from .common import create_loggers, parse_config
from ebu_tt_live.consumers import ConsumerFactory
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live import bindings
from zope.interface import registry, adapter
from twisted.python import components
from itertools import cycle
from time import sleep


log = logging.getLogger('ebu_simple_consumer')
parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')

items = [1,2,3,4,5,6,7]


def main():
    args = parser.parse_args()
    create_loggers()
    log.info('This is a Simple Consumer example')

    clock = LocalMachineClock()

    def gen_time():
        while True:
            yield clock.get_full_clock_time()

    bla = 0
    for item in gen_time():
        print item
        bla += 1
        sleep(0.2)
        if bla > 20:
            break
