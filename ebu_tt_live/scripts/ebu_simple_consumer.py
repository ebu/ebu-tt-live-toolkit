import logging
from argparse import ArgumentParser
from .common import create_loggers

from ebu_tt_live.node import SimpleConsumer
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.twisted import TwistedConsumer, BroadcastClientFactory, ClientNodeProtocol
from ebu_tt_live.carriage.twisted import TwistedConsumerImpl
from ebu_tt_live.carriage.filesystem import FilesystemConsumerImpl, FilesystemReader
from twisted.internet import reactor


log = logging.getLogger('ebu_simple_consumer')


parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')
parser.add_argument('-m', '--manifest-path', dest='manifest_path',
                    help='Documents are read from the filesystem instead of the network, takes a manifest file as input',
                    type=str
                    )
parser.add_argument('-f', '--tail-f', dest='do_tail',
                    help='Works only with -m, if set the script will wait for new lines to be added to the file once the last line is reached. Exactly like tail -f does.',
                    action="store_true", default=False
                    )


def main():
    args = parser.parse_args()
    create_loggers()
    log.info('This is a Simple Consumer example')

    manifest_path = args.manifest_path
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

    simple_consumer = SimpleConsumer(
        node_id='simple-consumer',
        carriage_impl=consumer_impl,
        reference_clock=reference_clock
    )

    if manifest_path:
        fs_reader.resume_reading()
    else:
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
