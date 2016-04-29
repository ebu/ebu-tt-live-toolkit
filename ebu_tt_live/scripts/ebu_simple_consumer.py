import logging
from argparse import ArgumentParser
from .common import create_loggers, parse_config
from ebu_tt_live.consumers import ConsumerFactory
from ebu_tt_live import bindings
from zope.interface import registry, adapter
from twisted.python import components

log = logging.getLogger('ebu_simple_consumer')
parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')


def main():
    args = parser.parse_args()
    #config = parse_config(
    #    config=args.config,
    #    module_name='ebu_simple_consumer'
    #)
    create_loggers()
    log.info('This is a Simple Consumer example')
    #consumer = ConsumerFactory.create_consumer(
    #    config=config
    #)
    #consumer.start()

    adapter.
