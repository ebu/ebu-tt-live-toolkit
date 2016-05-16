import logging
from argparse import ArgumentParser
from .common import create_loggers
from ebu_tt_live.clocks.local import LocalMachineClock

from ebu_tt_live.node import SimpleConsumer
from ebu_tt_live.twisted import TwistedConsumerMixin, TwistedConsumer, BroadcastClientFactory, ClientNodeProtocol
from twisted.internet import reactor


log = logging.getLogger('ebu_simple_consumer')


parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')


class TwistedSimpleDocumentConsumer(TwistedConsumerMixin, SimpleConsumer):
    pass


def main():
    args = parser.parse_args()
    create_loggers()
    log.info('This is a Simple Consumer example')

    simple_consumer = TwistedSimpleDocumentConsumer(
        node_id='simple-consumer'
    )

    factory = BroadcastClientFactory(
        url='ws://localhost:9000',
        channels=['TestSequence1'],
        consumer=TwistedConsumer(
            custom_consumer=simple_consumer
        )
    )
    factory.protocol = ClientNodeProtocol

    factory.connect()

    reactor.run()
