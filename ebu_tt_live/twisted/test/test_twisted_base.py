
from twisted.trial.unittest import TestCase
from ebu_tt_live.twisted import base


class TestInterfaces(TestCase):

    def test_broadcaster(self):
        self.assertRaises(TypeError, base.IBroadcaster)
