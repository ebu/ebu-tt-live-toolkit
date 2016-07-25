"""
This file contains those bits and pieces that are necessary to give PyXB extra functionality.
"""

import threading
import logging

log = logging.getLogger(__name__)
xml_parsing_context = threading.local()


def get_xml_parsing_context():
    log.info('Accessing xml_parsing_context: {}'.format(xml_parsing_context))
    return xml_parsing_context.context


def reset_xml_parsing_context():
    log.info('Resetting xml_parsing_context: {}'.format(xml_parsing_context))
    xml_parsing_context.context = {}

reset_xml_parsing_context()
