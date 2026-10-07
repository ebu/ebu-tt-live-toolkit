
from unittest.mock import MagicMock

from twisted.trial.unittest import TestCase

from ebu_tt_live.twisted import TwistedWSConsumer, TwistedWSPushProducer


class TestTwistedConsumer(TestCase):

    def setUp(self):
        self._custom_consumer = MagicMock()

    def test_instantiate(self):
        instance = TwistedWSConsumer(self._custom_consumer)


class TestTwistedProducer(TestCase):

    def setUp(self):
        self._custom_producer = MagicMock()
        self._consumer = MagicMock()

    def test_instantiate(self):
        instance = TwistedWSPushProducer(custom_producer=self._custom_producer)

