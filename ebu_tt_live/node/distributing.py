from .base import Node
import logging


log = logging.getLogger(__name__)


class DistributingNode(Node):

    _reference_clock = None

    def __init__(self, node_id, carriage_impl, reference_clock):
        super(DistributingNode, self).__init__(node_id, carriage_impl)
        self._reference_clock = reference_clock

    def process_document(self, document, **kwargs):
        self._carriage_impl.emit_document(document, **kwargs)

    @property
    def reference_clock(self):
        return self._reference_clock

    @reference_clock.setter
    def reference_clock(self, value):
        self._reference_clock = value
