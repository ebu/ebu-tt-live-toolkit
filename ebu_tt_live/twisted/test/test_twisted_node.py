
from twisted.trial.unittest import TestCase
from ebu_tt_live.twisted.node import TwistedPushProducer, TwistedConsumer
from mock import MagicMock


class TestTwistedConsumer(TestCase):

    def setUp(self):
        self._custom_consumer = MagicMock()

    def test_instantiate(self):
        instance = TwistedConsumer(self._custom_consumer)


class TestTwistedProducer(TestCase):

    def setUp(self):
        self._custom_producer = MagicMock()
        self._consumer = MagicMock()

    def test_instantiate(self):
        instance = TwistedPushProducer(consumer=self._consumer, custom_producer=self._custom_producer)

