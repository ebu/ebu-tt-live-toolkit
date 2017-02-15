from .base import AbstractCombinedNode
from ebu_tt_live.documents import EBUTT3Document
import logging
import six

log = logging.getLogger(__name__)


class DistributingNode(AbstractCombinedNode):

    _reference_clock = None
    _expects = six.text_type
    _provides = six.text_type

    def __init__(self, node_id, reference_clock, producer_carriage=None, consumer_carriage=None, **kwargs):
        super(DistributingNode, self).__init__(
            node_id=node_id,
            consumer_carriage=consumer_carriage,
            producer_carriage=producer_carriage,
            **kwargs
        )
        self._reference_clock = reference_clock

    def process_document(self, document, **kwargs):
        self.producer_carriage.emit_data(data=document, **kwargs)

    @property
    def reference_clock(self):
        return self._reference_clock

    @reference_clock.setter
    def reference_clock(self, value):
        self._reference_clock = value
