
from Queue import Queue
from nltk.tokenize import PunktSentenceTokenizer, BlanklineTokenizer, WhitespaceTokenizer
from datetime import timedelta
from twisted.internet import task
from twisted.internet import reactor
from zope.interface import implementer
import sys
from twisted.python import log

from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.producers import IContentProducer
from ebu_tt_live.streaming import BroadcastServerFactory, StreamingServerProtocol
from ebu_tt_live.documents import EBUTT3Document, TimeBase
from ebu_tt_live.bindings import div_type, p_type, br_type


@implementer(IContentProducer)
class SimpleProducer(object):

    _clock = None
    _input_lines = None
    _scheduler = None
    _id_seq = None
    _broadcaster = None

    def __init__(self, reference_clock, input_blocks, scheduler):
        self._clock = reference_clock
        self._input_lines = input_blocks
        self._scheduler = scheduler
        self._id_seq = 1

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

    def register_broadcaster(self, broadcaster):
        self._broadcaster = broadcaster

    def stream_documents(self):
        # Fake a timed operation of a live feed.
        start_time = self._clock.get_time()
        current_delay = timedelta()

        for lines in self._input_lines:
            current_delay += timedelta(seconds=2)
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
            document.set_begin(self._clock.get_full_clock_time(start_time + current_delay))

            document.validate()

            self._id_seq += 1

            # self._scheduler.schedule(SimpleProducer._print_stuff, current_delay-timedelta(seconds=1), document)
            if self._broadcaster:
                self._scheduler.schedule(self.broadcast_document, current_delay-timedelta(seconds=1), document)

    def broadcast_document(self, document):
        self._broadcaster.broadcast(document.get_xml())

    @staticmethod
    def _print_stuff(document):
        print(document.get_xml())


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


class TwistedScheduler(object):

    _reactor = None

    def __init__(self, reactor):
        self._reactor = reactor

    def schedule(self, function, delay, *args, **kwargs):
        task.deferLater(self._reactor, delay.seconds, function, *args, **kwargs)


def main():
    log.startLogging(sys.stdout)

    reference_clock = LocalMachineClock()

    with open('blargh.txt', 'r') as infile:
        full_text = infile.read()

    subtitle_tokens = tokenize_english_document(full_text)

    producer = SimpleProducer(
        input_blocks=subtitle_tokens,
        reference_clock=reference_clock,
        scheduler=TwistedScheduler(reactor)
    )

    wsFactory = BroadcastServerFactory

    factory = wsFactory(u"ws://127.0.0.1:9000")

    factory.protocol = StreamingServerProtocol

    producer.register_broadcaster(factory)

    factory.listen()

    producer.stream_documents()

    reactor.run()
