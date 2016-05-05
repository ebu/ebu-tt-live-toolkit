
from Queue import Queue
from nltk.tokenize import PunktSentenceTokenizer, BlanklineTokenizer, WhitespaceTokenizer
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.documents import EBUTT3Document, TimeBase
from ebu_tt_live.bindings import div_type, p_type, br_type


class SimpleProducer(object):

    _clock = None
    _document_queue = None
    _input_lines = None

    def __init__(self, reference_clock, input_file):
        self._clock = reference_clock
        self._document_queue = Queue()
        self._input_lines = input_file.split('\n')

    def _create_fragment(self, lines, begin, dur):
        # At this point we need to fix the timing format problems
        return div_type(
            p_type(
                *zip(lines, lambda x: br_type())
            ),
            begin=begin,
            dur=dur
        )

    def stream_documents(self):
        while self._input_lines:
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
            print sentence
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
                    print current_line
                    lines.append(current_line)
                    current_line = ''
                    line_full = False

                if len(lines) >= lines_per_subtitle:
                    end_list.append(lines)
                    lines = []
            if lines:
                end_list.append(lines)

    return end_list


def main():

    reference_clock = LocalMachineClock()

    document = EBUTT3Document(
        time_base=TimeBase.CLOCK,
        sequence_identifier='testSequence',
        sequence_number=1,
        lang='en-GB'
    )

    with open('blargh.txt', 'r') as infile:
        full_text = infile.read()

    subtitle_tokens = tokenize_english_document(full_text)
    import ipdb
    ipdb.set_trace()


