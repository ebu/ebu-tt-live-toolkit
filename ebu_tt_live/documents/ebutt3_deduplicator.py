from datetime import timedelta
import logging
import copy
from pyxb.binding.basis import NonElementContent, ElementContent
from ebu_tt_live.bindings import tt


log = logging.getLogger(__name__)


class EBUTT3Deduplicator(object):

    _style_segment = None
    _style_list = []
    _new_label = None
    _sequence_number = None
    _sequence_identifier = None

    def __init__(self, style_segment, style_list, new_label, sequence_number, sequence_identifier):
        
