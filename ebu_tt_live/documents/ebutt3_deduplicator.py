from datetime import timedelta
import logging
import copy
from pyxb.binding.basis import NonElementContent, ElementContent
from ebu_tt_live.bindings import tt


log = logging.getLogger(__name__)


class EBUTT3Deduplicator(object):
