
from twisted.trial.unittest import TestCase
from twisted.test import proto_helpers
from twisted.internet import reactor
from ebu_tt_live.twisted.websocket import BroadcastServerFactory, BroadcastServerProtocol
from mock import MagicMock


class TestBroadcastServerFactory(TestCase):

    def setUp(self):
        self.factory = BroadcastServerFactory()
        self.proto = BroadcastServerProtocol()
        self.proto.factory = self.factory
        self.tr = proto_helpers.StringTransport()


    def tearDown(self):
        pass

    def test_connection_made(self):
        self.proto.makeConnection(self.tr)
