from datetime import timedelta
from logging import getLogger
import copy
from pyxb.binding.basis import NonElementContent, ElementContent
from ebu_tt_live.bindings import tt


log = logging.getLogger(__name__)


class EBUTT3Deduplicator(object):

    _style_id = None
    _style_attribute = None
    _sequence_identifier = None
    _sequence_number = None
    _dataset = None

    def __init__(self, style_id, style_attribute, sequence_identifier, sequence_number):
        if not style_id || style_attribute:
            raise Exception()
        self._style_id = list(style_id)
        self._style_attribute = list(style_attribute)
        self._sequence_idtentifier = sequence_identifier
        self._sequence_number = sequence_number
