
from itertools import cycle
from twisted.internet import task, reactor
from argparse import ArgumentParser
from .common import create_loggers
from ebu_tt_live.utils import tokenize_english_document

from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.examples import get_example_data
from ebu_tt_live.documents import EBUTT3DocumentSequence
from ebu_tt_live.node import SimpleProducer
from ebu_tt_live.twisted import BroadcastServerFactory, BroadcastServerProtocol, \
    TwistedWSPushProducer
from ebu_tt_live.carriage.filesystem import FilesystemProducerImpl
from ebu_tt_live.carriage.websocket import WebsocketProducerCarriage
from ebu_tt_live.adapters.node_carriage import ProducerNodeCarriageAdapter


parser = ArgumentParser()

parser.add_argument('--reference-clock', dest='reference_clock',
                    help='content should show reference clock times when the content was generated on the server',
                    action='store_true', default=False)

parser.add_argument('--folder-export', dest='folder_export',
                    help='export xml files to given folder',
                    type=str
                    )


def main():
    create_loggers()

    parsed_args = parser.parse_args()

    sequence_identifier = 'TestSequence1'

    do_export = False
    if parsed_args.folder_export:
        do_export = True

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'

    document_sequence = EBUTT3DocumentSequence(
        sequence_identifier=sequence_identifier,
        lang='en-GB',
        reference_clock=reference_clock
    )

    if parsed_args.reference_clock:
        subtitle_tokens = None  # Instead of text we provide the availability time as content.
    else:
        # Let's read our example conversation
        full_text = get_example_data('simple_producer.txt')
        if do_export:
            subtitle_tokens = iter(tokenize_english_document(full_text))
        else:
            # This makes the source cycle infinitely.
            subtitle_tokens = cycle(tokenize_english_document(full_text))

    # This object is used as flexible binding to the carriage mechanism and twisted integrated as dependency injection
    prod_impl = None
    if do_export:
        prod_impl = FilesystemProducerImpl(parsed_args.folder_export)
    else:
        prod_impl = WebsocketProducerCarriage()
        prod_impl.sequence_identifier = sequence_identifier

    simple_producer = SimpleProducer(
        node_id='simple-producer',
        producer_carriage=None,
        document_sequence=document_sequence,
        input_blocks=subtitle_tokens
    )

    # Chaining a converter
    ProducerNodeCarriageAdapter(
        producer_carriage=prod_impl,
        producer_node=simple_producer
    )

    if do_export:
        prod_impl.resume_producing()
    else:

        twisted_producer = TwistedWSPushProducer(
            custom_producer=prod_impl
        )

        factory = BroadcastServerFactory(
            url=u"ws://127.0.0.1:9000",
            producer=twisted_producer
        )

        factory.protocol = BroadcastServerProtocol

        factory.listen()

        # Here we schedule in the simple producer to create content responding to a periodic interval timer.
        looping_task = task.LoopingCall(simple_producer.process_document)

        looping_task.start(2.0)

        reactor.run()
