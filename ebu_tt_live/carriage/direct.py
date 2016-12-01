from .base import AbstractCombinedCarriage
from ebu_tt_live.utils import AnyType


class DirectCarriageImpl(AbstractCombinedCarriage):

    _expects = AnyType
    _provides = AnyType

    def on_new_data(self, data, **kwargs):
        self.consumer_node.on_new_data(data, **kwargs)

    def resume_producing(self):
        self.producer_node.resume_producing()

    def emit_data(self, data, **kwargs):
        self.producer_node.emit_data(data, **kwargs)
