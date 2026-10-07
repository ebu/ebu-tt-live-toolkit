
from pytest import fixture
from twisted.internet import reactor
from twisted.trial.unittest import TestCase

from ebu_tt_live.twisted import base


@fixture(autouse=True)
def clean_reactor():
    reactor.removeAll()


class TestInterfaces(TestCase):

    def test_broadcaster(self):
        self.assertRaises(TypeError, base.IBroadcaster)
