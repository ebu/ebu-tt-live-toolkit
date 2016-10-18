import logging
from argparse import ArgumentParser
from .common import create_loggers

from ebu_tt_live.node import EBUTTDEncoder
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.twisted import TwistedConsumer, BroadcastClientFactory, ClientNodeProtocol
from ebu_tt_live.carriage.twisted import TwistedConsumerImpl
from ebu_tt_live.carriage.filesystem import FilesystemConsumerImpl, FilesystemReader, SimpleFolderExport
from ebu_tt_live import bindings
from twisted.internet import task, reactor


log = logging.getLogger('ebu_simple_consumer')


parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')
parser.add_argument('-i', '--interval', dest='interval', metavar='INTERVAL',
                    type=float, default=1.0,
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
parser.add_argument('-z', '--clock-at-media-time-zero', dest='media_time_zero',
                    help='This sets the offset value that is used to turn clock time into media time.',
                    default='current', metavar='HH:MM:SS.mmm')
parser.add_argument('-o', '--output-folder', dest='output_folder', default='./')
parser.add_argument('-of', '--output-format', dest='output_format', default='xml')
parser.add_argument('--proxy', dest='proxy', help='HTTP Proxy server (http:// protocol not needed!)', type=str, metavar='ADDRESS:PORT')
parser.add_argument('--discard', dest='discard', help='Discard already converted documents', action='store_true', default=False)


def start_timer(encoder):
    segment_timer = task.LoopingCall(encoder.convert_next_segment)
    segment_timer.start(encoder.segment_length.total_seconds(), now=False)
    return segment_timer


def main():
    args = parser.parse_args()
    create_loggers()
    log.info('This is the EBU-TT-D encoder')

    manifest_path = args.manifest_path

    websocket_url = args.websocket_url
    websocket_channel = args.websocket_channel

    fs_reader = None

    if manifest_path:
        do_tail = args.do_tail
        consumer_impl = FilesystemConsumerImpl()
        fs_reader = FilesystemReader(manifest_path, consumer_impl, do_tail)
    else:
        consumer_impl = TwistedConsumerImpl()

    if args.output_format == 'xml':
        outbound_carriage = SimpleFolderExport(args.output_folder, 'ebuttd-encode-{}.xml')
    else:
        raise Exception('Invalid output format: {}'.format(args.output_format))

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'

    media_time_zero = \
        args.media_time_zero == 'current' and reference_clock.get_time() \
        or bindings.ebuttdt.LimitedClockTimingType(str(args.media_time_zero)).timedelta

    ebuttd_converter = EBUTTDEncoder(
        node_id='simple-consumer',
        carriage_impl=consumer_impl,
        outbound_carriage_impl=outbound_carriage,
        reference_clock=reference_clock,
        segment_length=args.interval,
        media_time_zero=media_time_zero,
        segment_timer=start_timer,
        discard=args.discard
    )

    if manifest_path:
        fs_reader.resume_reading()
        # TODO: Do segmentation in filesystem mode. Especially bad is the tail usecase #209
    else:
        factory_args = {}
        if args.proxy:
            proxyHost, proxyPort = args.proxy.split(':')
            factory_args['proxy'] = {'host': proxyHost, 'port': int(proxyPort)}
        factory = BroadcastClientFactory(
            url=websocket_url,
            channels=[websocket_channel],
            consumer=TwistedConsumer(
                custom_consumer=consumer_impl
            ),
            **factory_args
        )
        factory.protocol = ClientNodeProtocol

        factory.connect()

        reactor.run()
