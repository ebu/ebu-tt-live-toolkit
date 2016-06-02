
from itertools import cycle
from twisted.internet import task, reactor
from argparse import ArgumentParser
from .common import create_loggers, tokenize_english_document

from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.example_data import get_example_data
from ebu_tt_live.documents import EBUTT3DocumentSequence
from ebu_tt_live.node import SimpleProducer
from ebu_tt_live.twisted import BroadcastServerFactory as wsFactory, StreamingServerProtocol, \
    TwistedPullProducer, TwistedProducerMixin


parser = ArgumentParser()

parser.add_argument('--reference-clock', dest='reference_clock',
                    help='content should be reference clock times when the content was generated on the server',
                    action='store_true', default=False)


# Here we get our custom document producer mixed in with the twisted compatibility layer
# This allows our document related custom code to be detached from the network library layer
class TwistedSimpleDocumentProducer(TwistedProducerMixin, SimpleProducer):
    pass


def main():
    create_loggers()

    parsed_args = parser.parse_args()

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'

    document_sequence = EBUTT3DocumentSequence(
        sequence_identifier='TestSequence1',
        lang='en-GB',
        reference_clock=reference_clock
    )

    if parsed_args.reference_clock:
        subtitle_tokens = None  # Instead of text we provide the availability time as content.
    else:
        # Let's read our example conversation
        full_text = get_example_data('simple_producer.txt')
        # This makes the source cycle infinitely.
        subtitle_tokens = cycle(tokenize_english_document(full_text))

    factory = wsFactory(u"ws://127.0.0.1:9000")

    factory.protocol = StreamingServerProtocol

    factory.listen()

    simple_producer = TwistedSimpleDocumentProducer(
        node_id='simple-producer',
        document_sequence=document_sequence,
        input_blocks=subtitle_tokens
    )

    # We are using a pull producer because it is the looping_task timer that triggers the production from the websocket
    # level. Every time the factory gets a pull signal from the timer it tells the producer to generate data.
    TwistedPullProducer(
        consumer=factory,
        custom_producer=simple_producer
    )

    looping_task = task.LoopingCall(factory.pull)

    looping_task.start(2.0)

    reactor.run()
