
from itertools import cycle
from nltk.tokenize import PunktSentenceTokenizer, BlanklineTokenizer, WhitespaceTokenizer
from datetime import timedelta
from twisted.internet import task, reactor, interfaces
from zope.interface import implementer
from twisted.python import log
import logging
from argparse import ArgumentParser

from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.streaming import BroadcastServerFactory, StreamingServerProtocol
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

    def __init__(self, consumer, reference_clock, input_blocks):
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

        lines = self._input_lines.next()

        activation_time = self._clock.get_time() + timedelta(seconds=1)

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


def tokenize_english_document(input_text):
    """
    This is a crude tokenizer for input conversations in English.
    :param input_text:
    :return:
    """
    end_list = []
    block_tokenizer = BlanklineTokenizer()
    sentence_tokenizer = PunktSentenceTokenizer()
    word_tokenizer = WhitespaceTokenizer()
    # using the 38 characters in one line rule from ITV subtitle guidelines
    characters_per_line = 38
    lines_per_subtitle = 2

    blocks = block_tokenizer.tokenize(input_text)
    for block in blocks:
        # We have one speaker
        sentences = sentence_tokenizer.tokenize(block)
        # We have the sentences
        for sentence in sentences:
            words = word_tokenizer.tokenize(sentence)
            reverse_words = words[::-1]

            lines = []
            current_line = ''
            line_full = False
            while reverse_words:
                word = reverse_words.pop()
                longer_line = ' '.join([current_line, word]).strip()
                if len(longer_line) > characters_per_line and len(current_line):
                    # The longer line is overreaching boundaries
                    reverse_words.append(word)
                    line_full = True
                elif len(word) >= characters_per_line:
                    # Very long words
                    current_line = longer_line
                    line_full = True
                else:
                    current_line = longer_line

                if line_full:
                    lines.append(current_line)
                    current_line = ''
                    line_full = False

                if len(lines) >= lines_per_subtitle:
                    end_list.append(lines)
                    lines = []
            if current_line:
                lines.append(current_line)
            if lines:
                end_list.append(lines)

    return end_list


def main():
    log_observer = log.PythonLoggingObserver(loggerName='twisted')
    log_observer.start()
    logging.basicConfig(level=logging.INFO)

    parsed_args = parser.parse_args()

    reference_clock = LocalMachineClock()

    if parsed_args.reference_clock:

        def gen_time():
            while True:
                yield [reference_clock.get_full_clock_time()]

        subtitle_tokens = gen_time()
    else:
        with open('blargh.txt', 'r') as infile:
            full_text = infile.read()

        subtitle_tokens = cycle(tokenize_english_document(full_text))

    wsFactory = BroadcastServerFactory

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
