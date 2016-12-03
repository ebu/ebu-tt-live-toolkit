
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketServerFactory, WebSocketServerProtocol, \
    listenWS, WebSocketClientFactory, connectWS

from twisted.internet import interfaces
from zope.interface import implementer
from logging import getLogger
import json
import weakref

from .base import IBroadcaster


log = getLogger(__name__)


class UserInputServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        try:
            self.factory.write(payload)
        except Exception as e:
            self.sendMessage("ERROR: " + str(e))
            return
        self.sendMessage('SUCCESS')

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)

    def sendMessage(self, payload, isBinary=False, fragmentSize=None, sync=False, doNotCompress=False):
        super(UserInputServerProtocol, self).sendMessage(
            payload=payload,
            isBinary=isBinary,
            fragmentSize=fragmentSize,
            sync=sync,
            doNotCompress=doNotCompress
        )


@implementer(IBroadcaster, interfaces.IConsumer)
class UserInputServerFactory(WebSocketServerFactory):
    _consumer = None
    _clients = None

    def __init__(self, url, consumer):
        super(UserInputServerFactory, self).__init__(url, protocols=[13])
        self._consumer = consumer
        self._consumer.registerProducer(self, True)
        self._clients = []

    def write(self, data):
        self._consumer.write(data)

    def resumeProducing(self):
        pass

    def register(self, client):
        if client not in self._clients:
            log.info("registered client {}".format(client.peer))
            self._clients.append(client)

    def unregister(self, client):
        if client in self._clients:
            log.info("unregistered client {}".format(client.peer))
            self._clients.remove(client)

    def listen(self):
        listenWS(self)


class BroadcastServerProtocol(WebSocketServerProtocol):

    _sequence_identifiers = None

    def onOpen(self):
        slug = self.http_request_path
        if slug.count('/') > 1:
            self.dropConnection()
        else:
            self._sequence_identifier = slug.replace('/', '').strip()
            self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            pass

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

    def sendSequenceMessage(
            self, sequence_identifier, payload, isBinary=False, fragmentSize=None, sync=False, doNotCompress=False
        ):
        if sequence_identifier == self._sequence_identifier:
            super(BroadcastServerProtocol, self).sendMessage(
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
    _producers = None
    _push_producer = None

    def __init__(self, url):
        super(BroadcastServerFactory, self).__init__(url, protocols=[13])
        self._clients = []
        self._producers = weakref.WeakSet()

    def registerProducer(self, producer, streaming):
        self._producers.add(producer)
        self._push_producer = streaming

    def unregisterProducer(self, producer=None):
        if producer is None:
            producer.stopProducing()
            self._producers.clear()
        if producer in self._producers:
            producer.stopProducing()
            self._producers.remove(producer)

    def write(self, sequence_identifier, data):
        self.broadcast(sequence_identifier, data)

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

    def broadcast(self, sequence_identifier, msg):
        log.info("broadcasting message...")

        for c in self._clients:
            c.sendSequenceMessage(sequence_identifier, msg.encode("utf-8"), isBinary=False, doNotCompress=False, sync=False)

    def stopFactory(self):
        self.unregisterProducer()

    def listen(self):
        listenWS(self)


class BroadcastClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        for sequence_identifier in self.factory.sequence_identifiers:
            self.subscribesequence_identifier(sequence_identifier)

    def subscribesequence_identifier(self, sequence_identifier):
        data = {
            'subscribe': sequence_identifier
        }
        self.sendMessage(json.dumps(data))

    def unsubscribesequence_identifier(self, sequence_identifier):
        data = {
            'unsubscribe': sequence_identifier
        }
        self.sendMessage(json.dumps(data))

    def onMessage(self, payload, isBinary):
        self.factory.dataReceived(payload)


@implementer(interfaces.IPushProducer)
class BroadcastClientFactory(WebSocketClientFactory):

    _sequence_identifiers = None
    _consumer = None
    _stopped = None

    def __init__(self, url, consumer, sequence_identifiers=None, *args, **kwargs):
        super(BroadcastClientFactory, self).__init__(url=url, *args, **kwargs)

        if not sequence_identifiers:
            self._sequence_identifiers = []
        else:
            self._sequence_identifiers = sequence_identifiers

        self._consumer = consumer
        self._consumer.registerProducer(self, True)
        self._stopped = True

    @property
    def sequence_identifiers(self):
        return self._sequence_identifiers

    @sequence_identifiers.setter
    def sequence_identifiers(self, value):
        self._sequence_identifiers = value

    def dataReceived(self, data):
        self._consumer.write(data)

    def stopProducing(self):
        self._stopped = True

    def resumeProducing(self):
        self._stopped = False

    def pauseProducing(self):
        self._stopped = True

    def connect(self):
        log.info('Connecting to {}'.format(self.url))
        connectWS(self)
