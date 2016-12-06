
from twisted.trial.unittest import TestCase
from ebu_tt_live.twisted.websocket import BroadcastServerFactory, BroadcastServerProtocol
from mock import MagicMock


class TestBroadcastServerFactory(TestCase):

    def setUp(self):
        self.factory = BroadcastServerFactory()
        self.proto = BroadcastServerProtocol()
        self.proto.factory = self.factory
        self.proto.log = MagicMock()

    def tearDown(self):
        pass

    def test_connection_made(self):
        pass
