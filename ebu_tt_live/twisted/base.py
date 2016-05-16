
from zope.interface import Interface


class IBroadcaster(Interface):

    def broadcast(self, channel, msg):
        """
        Broadcast message to all connected clients.
        :param channel:
        :param msg:
        :return:
        """
        raise NotImplementedError()

    def register(self, client):
        """
        Register new client on connection opening.
        :param client:
        :return:
        """
        raise NotImplementedError()

    def unregister(self, client):
        """
        Remove client from clients list on connection loss.
        :param client:
        :return:
        """
        raise NotImplementedError()
