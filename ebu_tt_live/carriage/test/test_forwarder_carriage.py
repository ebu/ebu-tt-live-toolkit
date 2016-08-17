from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.carriage.forwarder_carriage import ForwarderCarriageImpl


class TestForwarderCarriageImpl(TestCase):

    def setUp(self):
        self.consumer_impl = MagicMock()
        self.producer_impl = MagicMock()
        self.node = MagicMock()

    def test_register(self):
        forwarder_impl = ForwarderCarriageImpl(self.consumer_impl, self.producer_impl)
        forwarder_impl.register(self.node)
        self.consumer_impl.register.assert_called_with(self.node)
        self.producer_impl.register.assert_called_with(self.node)

    def test_emit_document(self):
        forwarder_impl = ForwarderCarriageImpl(self.consumer_impl, self.producer_impl)
        document = MagicMock()
        forwarder_impl.emit_document(document)
        self.producer_impl.emit_document.assert_called_with(document)

    def test_on_new_data(self):
        forwarder_impl = ForwarderCarriageImpl(self.consumer_impl, self.producer_impl)
        data = MagicMock()
        forwarder_impl.on_new_data(data)
        self.consumer_impl.on_new_data.assert_called_with(data)
