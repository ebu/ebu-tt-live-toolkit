import logging
from argparse import ArgumentParser
from .common import create_loggers

from ebu_tt_live.node import SimpleConsumer
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.twisted import TwistedConsumer, UserInputServerProtocol, UserInputServerFactory
from ebu_tt_live.carriage.twisted import TwistedConsumerImpl
from twisted.internet import reactor


log = logging.getLogger('ebu_simple_consumer')


parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')


def main():
    args = parser.parse_args()
    create_loggers()
    log.info('This is a Simple Consumer example')

    consumer_impl = None

    consumer_impl = TwistedConsumerImpl()

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'

    simple_consumer = SimpleConsumer(
        node_id='simple-consumer',
        carriage_impl=consumer_impl,
        reference_clock=reference_clock
    )

    factory = UserInputServerFactory(
        url='ws://127.0.0.1:9001',
        consumer=TwistedConsumer(
            custom_consumer=consumer_impl
        )
    )
    factory.protocol = UserInputServerProtocol

    factory.listen()

    reactor.run()
