import logging
from argparse import ArgumentParser
from .common import create_loggers

from ebu_tt_live.node import EBUTTDEncoder
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.twisted import TwistedConsumer, BroadcastClientFactory, ClientNodeProtocol
from ebu_tt_live.carriage.twisted import TwistedConsumerImpl
from ebu_tt_live.carriage.filesystem import FilesystemConsumerImpl, FilesystemReader
from twisted.internet import task, reactor


log = logging.getLogger('ebu_simple_consumer')


parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')
parser.add_argument('-i', '--interval', dest='interval', metavar='INTERVAL',
                    type=float, default=2.0,
                    help='Segmentation interval')
parser.add_argument('-m', '--manifest-path', dest='manifest_path',
                    help='Documents are read from the filesystem instead of the network, takes a manifest file as input',
                    type=str
                    )
parser.add_argument('-u', '--websocket-url', dest='websocket_url',
                    help='URL for the websocket address to connect to',
                    default='ws://localhost:9000')
parser.add_argument('-s', '--websocket-channel', dest='websocket_channel',
                    help='Channel to connect to for websocket',
                    default='TestSequence1')
parser.add_argument('-f', '--tail-f', dest='do_tail',
                    help='Works only with -m, if set the script will wait for new lines to be added to the file once the last line is reached. Exactly like tail -f does.',
                    action="store_true", default=False
                    )


def main():
    args = parser.parse_args()
    create_loggers()
    log.info('This is a Simple Consumer example')

    manifest_path = args.manifest_path

    websocket_url = args.websocket_url
    websocket_channel = args.websocket_channel

    consumer_impl = None
    fs_reader = None

    if manifest_path:
        do_tail = args.do_tail
        consumer_impl = FilesystemConsumerImpl()
        fs_reader = FilesystemReader(manifest_path, consumer_impl, do_tail)
    else:
        consumer_impl = TwistedConsumerImpl()

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'

    ebuttd_converter = EBUTTDEncoder(
        node_id='simple-consumer',
        carriage_impl=consumer_impl,
        reference_clock=reference_clock,
        segment_length=args.interval
    )

    if manifest_path:
        fs_reader.resume_reading()
        # TODO: Do segmentation in filesystem mode. Especially bad is the tail usecase #209
    else:
        factory = BroadcastClientFactory(
            url=websocket_url,
            channels=[websocket_channel],
            consumer=TwistedConsumer(
                custom_consumer=consumer_impl
            )
        )
        factory.protocol = ClientNodeProtocol

        factory.connect()

        segment_timer = task.LoopingCall(ebuttd_converter.convert_next_segment)
        segment_timer.start(args.interval)

        reactor.run()
