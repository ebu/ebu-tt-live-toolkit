
from itertools import cycle
from datetime import timedelta
from twisted.internet import task, reactor, interfaces
from zope.interface import implementer
from twisted.python import log
import logging
from argparse import ArgumentParser
from .common import create_loggers, tokenize_english_document

from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.streaming import BroadcastServerFactory as wsFactory, StreamingServerProtocol
from ebu_tt_live.documents import EBUTT3Document, TimeBase
from ebu_tt_live.bindings import div_type, p_type, br_type


parser = ArgumentParser()

parser.add_argument('--reference-clock', dest='reference_clock',
                    help='content should be reference clock times when the content was generated on the server',
                    action='store_true', default=False)


@implementer(interfaces.IPullProducer)
class SimplePullDocumentProducer(object):

    _clock = None
    _input_lines = None
    _id_seq = None
    _consumer = None

    def __init__(self, consumer, reference_clock, input_blocks=None):
        self._clock = reference_clock
        self._input_lines = input_blocks
        self._id_seq = 1
        self._consumer = consumer

        self._consumer.registerProducer(self, False)

    def _interleave_line_breaks(self, items):
        end_list = []
        for item in items:
            end_list.append(item)
            end_list.append(br_type())
        end_list.pop()
        return end_list

    def _create_fragment(self, lines):
        return div_type(
            p_type(
                *self._interleave_line_breaks(lines),
                id='ID{:03d}'.format(1)
            )
        )

    def resumeProducing(self):

        activation_time = self._clock.get_time() + timedelta(seconds=1)

        if self._input_lines:
            lines = self._input_lines.next()
        else:
            lines = [activation_time]

        document = EBUTT3Document(
            time_base=TimeBase.CLOCK,
            sequence_identifier='testSequence',
            sequence_number=self._id_seq,
            lang='en-GB'
        )

        document.add_div(
            self._create_fragment(
                lines
            )
        )

        document.set_dur('1s')
        document.set_begin(self._clock.get_full_clock_time(activation_time))

        document.validate()

        self._id_seq += 1

        self._consumer.write(document.get_xml())

    def stopProducing(self):
        pass


def main():
    create_loggers()

    parsed_args = parser.parse_args()

    reference_clock = LocalMachineClock()

    if parsed_args.reference_clock:
        subtitle_tokens = None  # Instead of text we provide the availability time as content.
    else:
        # Let's read our example conversation
        with open('blargh.txt', 'r') as infile:
            full_text = infile.read()
        # This makes the source cycle infinitely.
        subtitle_tokens = cycle(tokenize_english_document(full_text))

    factory = wsFactory(u"ws://127.0.0.1:9000")

    factory.protocol = StreamingServerProtocol

    factory.listen()

    SimplePullDocumentProducer(
        consumer=factory,
        input_blocks=subtitle_tokens,
        reference_clock=reference_clock
    )

    looping_task = task.LoopingCall(factory.pull)

    looping_task.start(2.0)

    reactor.run()
