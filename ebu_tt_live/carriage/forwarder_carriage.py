from .base import AbstractCombinedCarriage


class ForwarderCarriageImpl(AbstractCombinedCarriage):

    _consumer_carriage = None
    _producer_carriage = None

    def __init__(self, consumer_carriage, producer_carriage):
        self._consumer_carriage = consumer_carriage
        self._producer_carriage = producer_carriage

    def register_node(self, node):
        self._node = node
        self._consumer_carriage.register(node)
        self._producer_carriage.register(node)

    def emit_data(self, data, **kwargs):
        self._producer_carriage.emit_data(data)

    def on_new_data(self, data, **kwargs):
        self._consumer_carriage.on_new_data(data)
