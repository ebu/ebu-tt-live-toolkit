import logging
from argparse import ArgumentParser
from .common import create_loggers

from ebu_tt_live.node import EBUTTDConverterConsumer
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.twisted import TwistedConsumer, BroadcastClientFactory, ClientNodeProtocol
from ebu_tt_live.carriage.twisted import TwistedConsumerImpl
from twisted.internet import task, reactor


log = logging.getLogger('ebu_simple_consumer')


parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')
parser.add_argument('-i', '--interval', dest='interval', metavar='INTERVAL', type=float, default=2.0)


def main():
    args = parser.parse_args()
    create_loggers()
    log.info('This is a Simple Consumer example')


    consumer_impl = TwistedConsumerImpl()

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'

    ebuttd_converter = EBUTTDConverterConsumer(
        node_id='simple-consumer',
        carriage_impl=consumer_impl,
        reference_clock=reference_clock
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

    segment_timer = task.LoopingCall(ebuttd_converter.convert_next_segment)
    segment_timer.start(args.interval)

    reactor.run()
