from .base import CombinedCarriageImpl


class ForwarderCarriageImpl(CombinedCarriageImpl):

    _consumer_carriage = None
    _producer_carriage = None

    def __init__(self, consumer_carriage, producer_carriage):
        self._consumer_carriage = consumer_carriage
        self._producer_carriage = producer_carriage

    def register(self, node):
        self._node = node
        self._consumer_carriage.register(node)
        self._producer_carriage.register(node)

    def emit_document(self, document):
        self._producer_carriage.emit_document(document)

    def on_new_data(self, data):
        self._consumer_carriage.on_new_data(data)
