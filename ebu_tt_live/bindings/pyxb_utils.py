"""
This file contains those bits and pieces that are necessary to give PyXB extra functionality.
"""

import threading
import logging

log = logging.getLogger(__name__)

__xml_parsing_context = threading.local()
__xml_parsing_context.parsing = False


def get_xml_parsing_context():
    """
    The parsing context is a simple python dictionary that helps tie together semantic rules at parsing time.

    For example: making sure that limitedClockTimingtype and fullClockTimingType are instantiated appropriately taking
    into account the timeBase attribute on the tt element. In that case when the timeBase element is encountered by the
    parser is is added to the parsing context object to help PyXB make the right type in the timingType union.

    :return: dict that is te parsing context for the currently running parser
    :return: None if not in parsing mode
    """
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
    """
    This context manager is helpful to inject a thread local parsing context into the XML parser to be able to control
    its type choices based on semantic rules. The context manager makes sure the context is renewed every time a new
    document is parsed. This prevents unwanted correlation between documents.
    """

    def __enter__(self):
        reset_xml_parsing_context(True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        reset_xml_parsing_context()
