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

    def process_document(self, document, sequence_identifier=None, **kwargs):
        if sequence_identifier is None:
            doc = EBUTT3Document.create_from_xml(document)
            sequence_identifier = doc.sequence_identifier
        self.producer_carriage.emit_data(data=document, sequence_identifier=sequence_identifier, **kwargs)

    @property
    def reference_clock(self):
        return self._reference_clock

    @reference_clock.setter
    def reference_clock(self, value):
        self._reference_clock = value
