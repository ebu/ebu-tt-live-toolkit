import logging
from argparse import ArgumentParser
from .common import create_loggers

from ebu_tt_live.node import SimpleConsumer
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.twisted import TwistedConsumer, BroadcastClientFactory, ClientNodeProtocol
from ebu_tt_live.carriage.twisted import TwistedConsumerImpl, TwistedCorrectorConsumerImpl
from ebu_tt_live.carriage.filesystem import FilesystemConsumerImpl, FilesystemReader
from twisted.internet import reactor


log = logging.getLogger('ebu_simple_consumer')


parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')
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
parser.add_argument('--correct', dest='correct', help='Correct demo feed errors', action='store_true', default=False)
parser.add_argument('--proxy', dest='proxy', help='HTTP Proxy server (http:// protocol not needed!)', type=str, metavar='ADDRESS:PORT')


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
        if args.correct:
            consumer_impl = TwistedCorrectorConsumerImpl()
        else:
            consumer_impl = TwistedConsumerImpl()

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'

    simple_consumer = SimpleConsumer(
        node_id='simple-consumer',
        carriage_impl=consumer_impl,
        reference_clock=reference_clock
    )

    if manifest_path:
        fs_reader.resume_reading()
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
