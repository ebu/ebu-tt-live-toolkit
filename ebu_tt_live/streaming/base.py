
from zope.interface import Interface


class IBroadcaster(Interface):

    def broadcast(self, msg):
        raise NotImplementedError()

    def register(self, client):
        raise NotImplementedError()

    def unregister(self, client):
        raise NotImplementedError()
