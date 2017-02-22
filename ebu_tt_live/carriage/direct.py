from .base import AbstractCombinedCarriage
from ebu_tt_live.utils import ANY


class DirectCarriageImpl(AbstractCombinedCarriage):

    _expects = ANY
    _provides = ANY

    def on_new_data(self, data, **kwargs):
        self.producer_node.emit_data(data, **kwargs)

    def resume_producing(self):
        self.producer_node.resume_producing()

    def emit_data(self, data, **kwargs):
        self.consumer_node.process_document(data, **kwargs)
