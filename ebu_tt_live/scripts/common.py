
import logging
from configobj import ConfigObj
import yaml
from nltk.tokenize import PunktSentenceTokenizer, BlanklineTokenizer, WhitespaceTokenizer
import re
from twisted.python import log as twisted_log


log = logging.getLogger(__name__)
log_format = '[%(levelname)s] (%(asctime)s) in %(name)s[%(lineno)d] - %(message)s'
yaml_file = re.compile('^.*(\.yml|\.yaml)(\w)?$')


def create_loggers(level=logging.INFO):
    # Pipe Twisted's loggers into python logging package
    log_observer = twisted_log.PythonLoggingObserver()
    log_observer.start()
    # Python logging setup
    # TODO: Make this configurable (https://github.com/bbc/ebu-tt-live-toolkit/issues/15)
    logging.basicConfig(level=level, format=log_format)


def parse_config(config, module_name=None):
    import ipdb; ipdb.set_trace()
    if yaml_file.match(config):
        log.info('YAML config mode')
    return None


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
