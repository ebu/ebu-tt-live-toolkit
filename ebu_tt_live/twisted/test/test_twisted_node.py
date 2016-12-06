
from twisted.trial.unittest import TestCase
from ebu_tt_live.twisted.node import TwistedPushProducer, TwistedConsumer
from mock import MagicMock


class TestTwistedNodes(TestCase):

    def setUp(self):
        self._custom_consumer = MagicMock()

    def test_consumer_instantiate(self):
        instance = TwistedConsumer(self._custom_consumer)


