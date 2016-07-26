"""
This file contains those bits and pieces that are necessary to give PyXB extra functionality.
"""

import threading
import logging

log = logging.getLogger(__name__)

__xml_parsing_context = threading.local()
__xml_parsing_context.parsing = False


def get_xml_parsing_context():
    log.info('Accessing xml_parsing_context: {}'.format(__xml_parsing_context))
    if __xml_parsing_context.parsing is False:
        # We are not in parsing mode
        return None
    return __xml_parsing_context.context


def reset_xml_parsing_context(parsing=False):
    log.info('Resetting xml_parsing_context: {}'.format(__xml_parsing_context))
    __xml_parsing_context.context = {}
    __xml_parsing_context.parsing = parsing


class xml_parsing_context(object):

    def __enter__(self):
        reset_xml_parsing_context(True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        reset_xml_parsing_context()
