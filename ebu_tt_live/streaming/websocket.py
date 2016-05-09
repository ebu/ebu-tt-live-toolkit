
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from twisted.internet import interfaces
from zope.interface import implementer
from logging import getLogger

from .base import IBroadcaster


log = getLogger(__name__)


class StreamingServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        print(payload)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


@implementer(IBroadcaster, interfaces.IConsumer)
class BroadcastServerFactory(WebSocketServerFactory):
    _clients = None
    _producer = None
    _push_producer = None

    def __init__(self, url):
        super(BroadcastServerFactory, self).__init__(url, protocols=[13])
        self._clients = []

    def registerProducer(self, producer, streaming):
        self._producer = producer
        self._push_producer = streaming

    def unregisterProducer(self):
        self._producer.stopProducing()
        self._producer = None

    def write(self, data):
        self.broadcast(data)

    def register(self, client):
        if client not in self._clients:
            log.info("registered client {}".format(client.peer))
            self._clients.append(client)

    def unregister(self, client):
        if client in self._clients:
            log.info("unregistered client {}".format(client.peer))
            self._clients.remove(client)

    def pull(self):
        if self._producer:
            self._producer.resumeProducing()

    def broadcast(self, msg):
        log.info("broadcasting message...")

        for c in self._clients:
            c.sendMessage(msg.encode("utf-8"), isBinary=False, doNotCompress=False, sync=False)
            log.info("message sent to {}".format(c.peer))

    def stopFactory(self):
        self.unregisterProducer()

    def listen(self):
        listenWS(self)
