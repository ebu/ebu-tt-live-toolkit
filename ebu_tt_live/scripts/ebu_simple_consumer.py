# NOTE: This script is no longer maintained. Use `ebu-run` instead.

import logging
from argparse import ArgumentParser
from .common import create_loggers

from ebu_tt_live.node import SimpleConsumer
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.twisted import TwistedWSConsumer, BroadcastClientFactory, BroadcastClientProtocol
from ebu_tt_live.carriage.websocket import WebsocketConsumerCarriage
from ebu_tt_live.carriage.filesystem import FilesystemConsumerImpl, FilesystemReader
from ebu_tt_live.adapters.node_carriage import ConsumerNodeCarriageAdapter
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
                    default='ws://localhost:9000/TestSequence1/subscribe')
parser.add_argument('-f', '--tail-f', dest='do_tail',
                    help='Works only with -m, if set the script will wait for new lines to be added to the file once the last line is reached. Exactly like tail -f does.',
                    action="store_true", default=False
                    )
parser.add_argument('--proxy', dest='proxy', help='HTTP Proxy server (http:// protocol not needed!)', type=str, metavar='ADDRESS:PORT')


def main():
    args = parser.parse_args()
    create_loggers()
    log.info('This is a Simple Consumer example')

    manifest_path = args.manifest_path
    websocket_url = args.websocket_url
    consumer_impl = None
    fs_reader = None

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'

    if manifest_path:
        do_tail = args.do_tail
        consumer_impl = FilesystemConsumerImpl(reference_clock)
        fs_reader = FilesystemReader(manifest_path, consumer_impl, do_tail)
    else:
        consumer_impl = WebsocketConsumerCarriage()

    simple_consumer = SimpleConsumer(
        node_id='simple-consumer',
        reference_clock=reference_clock
    )

    # Chaining converter
    ConsumerNodeCarriageAdapter(
        consumer_node=simple_consumer,
        consumer_carriage=consumer_impl
    )

    if manifest_path:
        fs_reader.resume_reading()
    else:
        factory_args = {}
        if args.proxy:
            proxyHost, proxyPort = args.proxy.split(':')
            factory_args['proxy'] = {'host': proxyHost, 'port': int(proxyPort)}

        twisted_consumer = TwistedWSConsumer(
            custom_consumer=consumer_impl
        )

        factory = BroadcastClientFactory(
            url=websocket_url,
            consumer=twisted_consumer,
            **factory_args
        )

        factory.protocol = BroadcastClientProtocol

        factory.connect()

        reactor.run()
