import logging
from argparse import ArgumentParser
from .common import create_loggers

from ebu_tt_live.node.distributing import DistributingNode
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.twisted import TwistedConsumer, UserInputServerProtocol, UserInputServerFactory, BroadcastServerFactory, TwistedPullProducer, StreamingServerProtocol
from ebu_tt_live.carriage.forwarder_carriage import ForwarderCarriageImpl
from ebu_tt_live.carriage.filesystem import FilesystemProducerImpl
from ebu_tt_live.carriage.twisted import TwistedConsumerImpl, TwistedProducerImpl
from twisted.internet import reactor


log = logging.getLogger('ebu_simple_consumer')


parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')
parser.add_argument('-u', '--websocket-url', dest='websocket_url',
                    help='URL for the websocket address to connect to',
                    default='ws://127.0.0.1:9001')
parser.add_argument('--folder-export', dest='folder_export',
                    help='export xml files to given folder',
                    type=str
                    )


def main():
    args = parser.parse_args()
    create_loggers()

    do_export = False
    if args.folder_export:
        do_export = True

    sub_consumer_impl = TwistedConsumerImpl()
    sub_prod_impl = None
    if do_export:
        sub_prod_impl = FilesystemProducerImpl(args.folder_export)
    else:
        sub_prod_impl = TwistedProducerImpl()
    carriage_impl = ForwarderCarriageImpl(sub_consumer_impl, sub_prod_impl)

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'

    dist_node = DistributingNode(
        node_id='distributing-node',
        carriage_impl=carriage_impl,
        reference_clock=reference_clock
    )

    # This factory listens for incoming documents from the user input producer.
    user_input_server_factory = UserInputServerFactory(
        url=args.websocket_url,
        consumer=TwistedConsumer(
            custom_consumer=sub_consumer_impl
        )
    )
    user_input_server_factory.protocol = UserInputServerProtocol
    user_input_server_factory.listen()

    if not do_export:
        # This factory listens for any consumer to forward documents to.
        broadcast_factory = BroadcastServerFactory("ws://127.0.0.1:9000")
        broadcast_factory.protocol = StreamingServerProtocol
        broadcast_factory.listen()

        TwistedPullProducer(
            consumer=broadcast_factory,
            custom_producer=sub_prod_impl
        )

    reactor.run()
