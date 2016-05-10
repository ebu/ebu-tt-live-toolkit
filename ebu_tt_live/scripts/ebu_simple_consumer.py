import logging
from argparse import ArgumentParser
from .common import create_loggers
from ebu_tt_live.clocks.local import LocalMachineClock


log = logging.getLogger('ebu_simple_consumer')
parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')

items = [1,2,3,4,5,6,7]


def main():
    args = parser.parse_args()
    create_loggers()
    log.info('This is a Simple Consumer example')

    clock = LocalMachineClock()
