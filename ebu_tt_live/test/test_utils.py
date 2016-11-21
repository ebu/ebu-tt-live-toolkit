
from unittest import TestCase
from mock import MagicMock
from ebu_tt_live.utils import RingBufferWithCallback, RotatingFileBuffer


class TestRingBuffer(TestCase):

    maxlen = 3

    def setUp(self):
        self.callback = MagicMock()
        self.instance = RingBufferWithCallback(
            maxlen=self.maxlen,
            callback=self.callback
        )

    def test_add_one_item(self):
        self.instance.append(1)
        self.callback.assert_not_called()

    def test_add_three_items(self):
        self.instance.append(1)
        self.instance.append(2)
        self.instance.append(3)
        self.callback.assert_not_called()

    def test_add_four_items(self):
        self.test_add_three_items()
        self.instance.append(4)
        self.callback.assert_called_with(1)

    def test_add_five_items(self):
        self.test_add_four_items()
        self.instance.append(5)
        self.callback.assert_called_with(2)
