
from twisted.trial.unittest import TestCase
from twisted.internet import reactor
from ebu_tt_live.twisted import base
from pytest import fixture


@fixture(autouse=True)
def clean_reactor():
    reactor.removeAll()


class TestInterfaces(TestCase):

    def test_broadcaster(self):
        self.assertRaises(TypeError, base.IBroadcaster)
