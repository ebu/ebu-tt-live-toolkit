
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from twisted.internet import interfaces
from zope.interface import implementer
from logging import getLogger
import json

from .base import IBroadcaster


log = getLogger(__name__)


class StreamingServerProtocol(WebSocketServerProtocol):

    _channels = None

    def onOpen(self):
        self.factory.register(self)
        self._channels = set()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            try:
                data = json.loads(payload)
                if 'subscribe' in data:
                    log.info('{} subscibes to {}'.format(self.peer, data['subscribe']))
                    self._channels.add(data['subscribe'])
                if 'unsubscribe' in data:
                    log.info('{} unsubscribes from {}'.format(self.peer, data['unsubscribe']))
                    self._channels.remove(data['unsubscribe'])
            except Exception:
                pass

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

    def sendMessageOnChannel(self, channel, payload, isBinary=False, fragmentSize=None, sync=False, doNotCompress=False):
        if channel in self._channels:
            super(StreamingServerProtocol, self).sendMessage(
                payload=payload,
                isBinary=isBinary,
                fragmentSize=fragmentSize,
                sync=sync,
                doNotCompress=doNotCompress
            )
            log.info("message sent to {}".format(self.peer))


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

    def write(self, channel, data):
        self.broadcast(channel, data)

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

    def broadcast(self, channel, msg):
        log.info("broadcasting message...")

        for c in self._clients:
            c.sendMessageOnChannel(channel, msg.encode("utf-8"), isBinary=False, doNotCompress=False, sync=False)

    def stopFactory(self):
        self.unregisterProducer()

    def listen(self):
        listenWS(self)
