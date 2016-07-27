import logging
from argparse import ArgumentParser
from .common import create_loggers

from ebu_tt_live.node import SimpleConsumer
from ebu_tt_live.twisted import TwistedConsumer, BroadcastClientFactory, ClientNodeProtocol
from ebu_tt_live.carriage.twisted import TwistedConsumerImpl
from twisted.internet import reactor


log = logging.getLogger('ebu_simple_consumer')


parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')


def main():
    args = parser.parse_args()
    create_loggers()
    log.info('This is a Simple Consumer example')

    consumer_impl = TwistedConsumerImpl()

    simple_consumer = SimpleConsumer(
        node_id='simple-consumer',
        carriage_impl=consumer_impl
    )

    factory = BroadcastClientFactory(
        url='ws://localhost:9000',
        channels=['TestSequence1'],
        consumer=TwistedConsumer(
            custom_consumer=consumer_impl
        )
    )
    factory.protocol = ClientNodeProtocol

    factory.connect()

    reactor.run()
