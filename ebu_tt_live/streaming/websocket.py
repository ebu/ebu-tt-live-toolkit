
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from zope.interface import implementer

from .base import IBroadcaster


class StreamingServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        print(payload)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


@implementer(IBroadcaster)
class BroadcastServerFactory(WebSocketServerFactory):
    _clients = None

    def __init__(self, url):
        super(BroadcastServerFactory, self).__init__(url, protocols=[13])
        self._clients = []

    def register(self, client):
        if client not in self._clients:
            print("registered client {}".format(client.peer))
            self._clients.append(client)

    def unregister(self, client):
        if client in self._clients:
            print("unregistered client {}".format(client.peer))
            self._clients.remove(client)

    def broadcast(self, msg):
        print("broadcasting message...")

        for c in self._clients:
            c.sendMessage(msg.encode("utf-8"), isBinary=False, doNotCompress=False, sync=False)
            print("message sent to {}".format(c.peer))

    def listen(self):
        listenWS(self)
